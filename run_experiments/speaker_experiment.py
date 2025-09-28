import re
import json
import numpy as np
from typing import List

from run_experiments.utils import get_last_token_prob


def trial(prompt_text: str) -> tuple[str, float]:
    
    target_probs = []
    for target in ["A", "B", "C", "D", "E"]:
        last_token, last_token_prob = get_last_token_prob(prompt_text + target)
        if last_token.strip() != target:
            target_probs.append(0)
        else:
            target_probs.append(last_token_prob)

    target_probs = np.array(target_probs)

    prob_distr = target_probs / target_probs.sum()
    return prob_distr.tolist()


def run_trials(inputs: List[dict]):
    for input_data in inputs:
        system_message = input_data["system_message"]
        for trial_item in input_data["trial_items"]:
            prompt = trial_item["prompt"]
            prompt_text = system_message + prompt
            prob_distr = trial(prompt_text)
            # change in place
            trial_item["prob_distr"] = prob_distr


def main():
    with open("data/out/prompts.json", encoding="utf-8") as f:
        all_inputs = json.load(f)
        pass