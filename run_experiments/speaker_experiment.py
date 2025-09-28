import json
import numpy as np
from typing import List, Optional
from tqdm import tqdm

from run_experiments.utils import get_last_token_prob


def trial(prompt_text: str, pbar: Optional[tqdm] = None) -> tuple[str, float]:
    
    target_probs = []
    for target in ["A", "B", "C", "D", "E"]:
        last_token, last_token_prob = get_last_token_prob(prompt_text + target)
        if last_token.strip() != target:
            target_probs.append(0)
        else:
            target_probs.append(last_token_prob)
        if pbar:
            pbar.update(1)

    target_probs = np.array(target_probs)

    prob_distr = target_probs / target_probs.sum()
    return prob_distr.tolist()


def run_trials(inputs: List[dict], pbar: Optional[tqdm] = None):
    for input_data in inputs:
        system_message = input_data["system_message"]
        for trial_item in input_data["trial_items"]:
            prompt = trial_item["prompt"]
            prompt_text = system_message + prompt
            prob_distr = trial(prompt_text, pbar=pbar)
            # change in place
            trial_item["prob_distr"] = prob_distr


def main():
    with open("data/out/prompts.json", encoding="utf-8") as f:
        all_inputs = json.load(f)
    for o_key, input_collection in all_inputs.items():    # real / synthetic
        for f_key, inputs in input_collection.items():    # plain / hearts

            inputs = inputs[:2]  # DEBUGGING


            pbar = tqdm(total=len(inputs) * 5, desc=f"{o_key}/{f_key}")
            run_trials(inputs, pbar=pbar)  # in-place change
            pbar.close()
    with open("data/out/prompts_speaker_exp.json", "w", encoding="utf-8") as f:
        json.dump(all_inputs, f, ensure_ascii=False, indent=4)