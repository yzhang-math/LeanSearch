#!/usr/bin/env python3
# vllm_server.py - Simple API server compatible with FunSearch for local LLM inference

import argparse
import logging
import os
import time
import asyncio
from typing import List, Optional, Dict, Any, Union
import json

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import vllm 
import uvicorn
import torch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="vLLM API Server for FunSearch")

# Global variables
model = None
request_queue = asyncio.Queue()
BATCH_SIZE = 8  # Default batch size
BATCH_TIMEOUT = 0.1  # Seconds to wait for batching before processing

class GenerationRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int = 2048
    system_prompt: Optional[str] = None
    stop: Optional[Union[str, List[str]]] = None

class GenerationResponse(BaseModel):
    text: str
    usage: Dict[str, int] = Field(default_factory=dict)

class BatchRequest:
    def __init__(self, request: GenerationRequest, future: asyncio.Future):
        self.request = request
        self.future = future

async def batch_processor():
    """Background task to process batched requests"""
    while True:
        # Collect batch of requests
        batch = []
        start_time = time.time()
        
        # Get the first request or wait
        first_request = await request_queue.get()
        batch.append(first_request)
        
        # Try to collect more requests until batch size or timeout
        try:
            while len(batch) < BATCH_SIZE and (time.time() - start_time) < BATCH_TIMEOUT:
                try:
                    # Wait for more requests but with a timeout
                    request = await asyncio.wait_for(
                        request_queue.get(), 
                        timeout=max(0, BATCH_TIMEOUT - (time.time() - start_time))
                    )
                    batch.append(request)
                except asyncio.TimeoutError:
                    # No more requests within timeout
                    break
        except Exception as e:
            logger.error(f"Error collecting batch: {str(e)}")
        
        # Process the batch
        if batch:
            batch_size = len(batch)
            logger.info(f"Processing batch of {batch_size} requests")
            
            try:
                # Prepare prompts and sampling parameters
                prompts = []
                sampling_params_list = []
                
                for batch_req in batch:
                    req = batch_req.request
                    full_prompt = req.prompt
                    if req.system_prompt:
                        full_prompt = f"{req.system_prompt}\n\n{req.prompt}"
                    
                    prompts.append(full_prompt)
                    
                    sampling_params = vllm.SamplingParams(
                        temperature=req.temperature,
                        top_p=req.top_p,
                        max_tokens=req.max_tokens,
                        stop=req.stop or [],
                    )
                    sampling_params_list.append(sampling_params)
                
                # Generate all completions in one batch
                outputs = model.generate(prompts, sampling_params_list)
                
                # Process results
                for i, batch_req in enumerate(batch):
                    generated_text = outputs[i].outputs[0].text
                    
                    # Rough estimate of token counts
                    prompt_tokens = len(batch_req.request.prompt) // 4
                    completion_tokens = len(generated_text) // 4
                    
                    response = GenerationResponse(
                        text=generated_text,
                        usage={
                            "prompt_tokens": prompt_tokens,
                            "completion_tokens": completion_tokens,
                            "total_tokens": prompt_tokens + completion_tokens,
                        }
                    )
                    
                    # Set the result
                    batch_req.future.set_result(response)
            
            except Exception as e:
                logger.error(f"Error processing batch: {str(e)}")
                # Set error for all requests in batch
                for batch_req in batch:
                    if not batch_req.future.done():
                        batch_req.future.set_exception(e)
            
            # Mark tasks as done in the queue
            for _ in range(len(batch)):
                request_queue.task_done()

@app.post("/generate", response_model=GenerationResponse)
async def generate(request: GenerationRequest):
    """Generate completions for the given prompt"""
    global model, request_queue
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please restart the server.")
    
    logger.info(f"Received generation request with prompt length: {len(request.prompt)}")
    
    # Create a future to get the result
    future = asyncio.Future()
    
    # Queue the request
    batch_req = BatchRequest(request, future)
    await request_queue.put(batch_req)
    
    # Wait for the result
    try:
        return await future
    except Exception as e:
        logger.error(f"Error during generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

def load_model(model_name: str, gpu_layers: int = None, quantization=None):
    """Load the model into memory"""
    global model
    
    logger.info(f"Loading model: {model_name}")
    
    try:
        # Add any specific vLLM parameters you need
        model_kwargs = {}
        if gpu_layers is not None:
            model_kwargs["gpu_memory_utilization"] = gpu_layers
        if quantization:
            model_kwargs["quantization"] = quantization
            
        model = vllm.LLM(model=model_name, **model_kwargs)
        logger.info(f"Model {model_name} loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise

async def run_server_test():
    """Run a simple test to verify the server is working properly"""
    logger.info("Running server test...")
    
    test_prompt = "Complete this sentence: The quick brown fox"
    
    # Create a test request
    test_request = GenerationRequest(
        prompt=test_prompt,
        temperature=0.7,
        max_tokens=20
    )
    
    try:
        # Use the same endpoint that external clients would use
        response = await generate(test_request)
        
        logger.info(f"Test completed successfully!")
        logger.info(f"Prompt: '{test_prompt}'")
        logger.info(f"Response: '{response.text}'")
        logger.info(f"Token usage: {response.usage}")
        return True
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False

@app.on_event("startup")
async def startup_event():
    """Start the batch processor when the server starts"""
    # Start the background batch processor
    asyncio.create_task(batch_processor())
    
    # Run a test
    test_result = await run_server_test()
    if not test_result:
        logger.warning("Server test failed, but continuing to run...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a vLLM API server for FunSearch")
    parser.add_argument("--model", type=str, default="Goedel-LM/Goedel-Prover-SFT", help="Model name or path")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--gpu-layers", type=float, default=None, help="GPU memory utilization (0.0-1.0)")
    parser.add_argument("--quantization", type=str, default=None, help="Quantization type (e.g., 'awq')")
    parser.add_argument("--batch-size", type=int, default=8, help="Maximum batch size for processing requests")
    parser.add_argument("--batch-timeout", type=float, default=1, help="Maximum time to wait for batching (seconds)")
    
    args = parser.parse_args()
    
    # Set batch parameters
    BATCH_SIZE = args.batch_size
    BATCH_TIMEOUT = args.batch_timeout
    
    torch.cuda.empty_cache()
    # Load the model
    load_model(args.model, args.gpu_layers, args.quantization)
    
    # Start the server
    uvicorn.run(app, host=args.host, port=args.port)