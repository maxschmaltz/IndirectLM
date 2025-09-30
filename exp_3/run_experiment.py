import aiohttp
import asyncio
import json
import numpy as np
from typing import Dict, Any, List

# --- Configuration ---
BASE_URL = "http://0.0.0.0:8000/v1"
MODEL_NAME = "Qwen/Qwen3-4B-Instruct-2507"
PROMPT_FILE = "exp3_profiled_prompts.json" # Your generated file (20160 entries, etc.)
OUTPUT_FILE = "exp3_final_results_with_logprobs_subset.json" # NOTE: Changed output file name
# SUBSET_SIZE = 640 # <-- LIMIT: Process only the first x requests

# --- Concurrency Control ---
# Limit concurrent requests to avoid network saturation, 
# although vLLM handles large internal batches.
SEMAPHORE = asyncio.Semaphore(8) 

# --- Inference Function ---

async def get_inference_output(prompt_text: str) -> Dict[str, Any]:
    """Sends a request to the vLLM API and extracts the predicted answer and top 10 log-probs."""

    url = f"{BASE_URL}/completions"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt_text,
        # vLLM maxes this out to 0.01, which is fine for deterministic output
        "temperature": 0.001, 
        "max_tokens": 1,        # Generate only the single integer answer
        "logprobs": 10,         # Capture the top 10 token probabilities
        "echo": True
    }

    async with SEMAPHORE:
        async with aiohttp.ClientSession() as session:
            try:
                # Increased timeout slightly for large CPU models
                async with session.post(url, headers=headers, json=payload, timeout=7200) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        print(f"API Error ({resp.status}): {error_text}")
                        # Return failure markers
                        return {"inferred_answer": "ERROR", "top_10_log_probs": {}}

                    response = await resp.json()
                    
                    # 1. Get the single predicted answer
                    inferred_answer = response["choices"][0]["text"].strip()
                    
                    # 2. Get the log-probs map for the *first* generated token (index -1 in logprobs array)
                    # This map contains {token_text: log_prob_value} for the top 10 tokens.
                    top_10_log_probs = response["choices"][0]["logprobs"]["top_logprobs"][-1]
                    
                    return {
                        "inferred_answer": inferred_answer,
                        "top_10_log_probs": top_10_log_probs
                    }
            
            except asyncio.TimeoutError:
                print("Request timed out.")
                return {"inferred_answer": "TIMEOUT", "top_10_log_probs": {}}

            except Exception as e:
                print(f"General Request Failure: {e}")
                return {"inferred_answer": "FAIL", "top_10_log_probs": {}}

# --- Main Execution Loop ---

async def main_inference_loop():
    print(f"Loading prompts from {PROMPT_FILE}...")
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            full_prompts_data = json.load(f)
    except FileNotFoundError:
        print(f"FATAL ERROR: Prompt file '{PROMPT_FILE}' not found. Please run the generation script first.")
        return

    # --- SUBSETTING DATA ---
    # all_prompts_data = full_prompts_data[:SUBSET_SIZE]
    all_prompts_data = full_prompts_data
    print(f"Loaded total prompts: {len(full_prompts_data)}")
    print(f"Restricting processing to the first {len(all_prompts_data)} prompts.")
    
    tasks = []
    for item in all_prompts_data:
        tasks.append(get_inference_output(item['prompt']))

    print(f"Submitting {len(tasks)} asynchronous requests to vLLM API...")
    
    # Run all tasks concurrently
    results_outputs = await asyncio.gather(*tasks)

    # Process and save results
    final_results = []
    
    total_tasks = len(results_outputs)
    print("\n--- Processing Results ---")

    for i, output in enumerate(results_outputs):
        # Merge the inference output with the original scenario metadata
        result = all_prompts_data[i]
        
        # Store the two required fields
        result['inferred_answer'] = output['inferred_answer']
        result['top_10_log_probs'] = output['top_10_log_probs']
        
        if (i + 1) % 20 == 0 or (i + 1) == total_tasks:
            print(f"Processed {i + 1} of {total_tasks} requests.")

        final_results.append(result)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_results, f, indent=4, ensure_ascii=False)
        
    print(f"\nInference complete. Results saved to {OUTPUT_FILE}")
    print(f"Total scenarios processed: {len(final_results)}")


if __name__ == "__main__":
    asyncio.run(main_inference_loop())
