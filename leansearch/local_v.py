#!/usr/bin/env python3
# vllm_server.py - Simple API server compatible with FunSearch for local LLM inference

import argparse
import logging
import os
from typing import List, Optional, Dict, Any, Union
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import vllm 
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="vLLM API Server for FunSearch")

# Global variable to hold our loaded model
model = None

class GenerationRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    top_p: float = 0.95
    max_tokens: int = 4096
    system_prompt: Optional[str] = None
    stop: Optional[Union[str, List[str]]] = None

class GenerationResponse(BaseModel):
    text: str
    usage: Dict[str, int] = Field(default_factory=dict)

@app.post("/generate", response_model=GenerationResponse)
async def generate(request: GenerationRequest):
    """Generate completions for the given prompt"""
    global model
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please restart the server.")
    
    logger.info(f"Received generation request with prompt length: {len(request.prompt)}")
    
    # Construct the prompt with system instruction if provided
    full_prompt = request.prompt
    if request.system_prompt:
        full_prompt = f"{request.system_prompt}\n\n{request.prompt}"
    
    # Set up sampling parameters
    sampling_params = vllm.SamplingParams(
        temperature=request.temperature,
        top_p=request.top_p,
        max_tokens=request.max_tokens,
        stop=request.stop or [],
    )
    
    try:
        # Generate the completion
        outputs = model.generate([full_prompt], sampling_params)
        generated_text = outputs[0].outputs[0].text
        
        # Rough estimate of token counts
        prompt_tokens = len(request.prompt) // 4  # Approximate!
        completion_tokens = len(generated_text) // 4  # Approximate!
        
        logger.info(f"Generated text with length: {len(generated_text)}")
        
        return GenerationResponse(
            text=generated_text,
            usage={
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            }
        )
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a vLLM API server for FunSearch")
    parser.add_argument("--model", type=str, default = "Goedel-LM/Goedel-Prover-SFT", help="Model name or path")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default= 8000, help="Port to bind the server to")
    parser.add_argument("--gpu-layers", type=float, default=None, help="GPU memory utilization (0.0-1.0)")
    parser.add_argument("--quantization", type=str, default= None, help="Quantization type (e.g., 'awq')")
    
    args = parser.parse_args()
    
    # Load the model
    args.model = "Goedel-LM/Goedel-Prover-SFT"
    args.host = "0.0.0.0"
    args.port = 8000
    load_model(args.model, args.gpu_layers, args.quantization)
    
    # Start the server
    uvicorn.run(app, host=args.host, port=args.port)