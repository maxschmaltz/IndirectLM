import json
import numpy as np
from typing import List, Optional
from tqdm import tqdm

from run_experiments.utils import get_last_token_prob, MODEL_NAME
import asyncio


async def trial(prompt_text: str, pbar: Optional[tqdm] = None) -> list[float]:
    target_probs = []
    for target in ["A", "B", "C", "D", "E"]:
        if pbar:
            pbar.update(1)
        last_token, last_token_prob = await get_last_token_prob(prompt_text + target)
        if last_token.strip() != target:
            target_probs.append(0)
        else:
            target_probs.append(last_token_prob)

    target_probs = np.array(target_probs)
    prob_distr = target_probs / target_probs.sum()
    return prob_distr.tolist()

async def run_trials(inputs: List[dict], pbar: Optional[tqdm] = None):
    for input_data in inputs:
            system_message = input_data["system_message"]
            for trial_item in input_data["trial_items"]:
                try:
                    prompt = trial_item["prompt"]
                    prompt_text = system_message + prompt
                    prob_distr = await trial(prompt_text, pbar=pbar)
                    trial_item["prob_distr"] = prob_distr
                    # retrieve prediction
                    pred = np.argmax(prob_distr) + 1  # 1-indexed
                    trial_item["pred"] = int(pred)
                except Exception as e:
                    trial_item["prob_distr"] = [0.0] * 5
                    trial_item["pred"] = None
                    trial_item["message"] = str(e)


async def main():
    with open("data/out/prompts.json", encoding="utf-8") as f:
        all_inputs = json.load(f)
    for o_key, input_collection in all_inputs.items():    # real / synthetic
        for f_key, inputs in input_collection.items():    # plain / hearts
            total = sum(len(item["trial_items"]) for item in inputs) * 5
            pbar = tqdm(total=total, desc=f"{o_key}/{f_key}")
            await run_trials(inputs, pbar=pbar)  # in-place change
            pbar.close()
    _model_name = MODEL_NAME.split("/")[-1]
    with open(f"data/out/prompts_speaker_exp_{_model_name}.json", "w", encoding="utf-8") as f:
        json.dump(all_inputs, f, ensure_ascii=False, indent=4)