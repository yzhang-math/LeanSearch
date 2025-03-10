#!/usr/bin/env python3
# test_vllm_api.py - Simple client to test the vLLM API server

import requests
import json
import argparse
import time

def test_api(host, port, prompt, temperature=0.7, max_tokens=50):
    """Send a test request to the vLLM API server"""
    url = f"http://{host}:{port}/generate"
    
    payload = {
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": 0.95
    }
    
    print(f"Sending request to {url}")
    print(f"Prompt: '{prompt}'")
    
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            elapsed_time = time.time() - start_time
            
            print("\n--- Response ---")
            print(f"Time: {elapsed_time:.2f} seconds")
            print(f"Text: {result['text']}")
            print(f"Usage: {result['usage']}")
            return True
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except Exception as e:
        print(f"Error sending request: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the vLLM API server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="API server host")
    parser.add_argument("--port", type=int, default=8000, help="API server port")
    parser.add_argument("--prompt", type=str, default="Explain the concept of quantum computing in simple terms.", 
                        help="Prompt to send to the API")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for generation")
    parser.add_argument("--max-tokens", type=int, default=100, help="Maximum tokens to generate")
    
    args = parser.parse_args()
    
    test_api(args.host, args.port, args.prompt, args.temperature, args.max_tokens)