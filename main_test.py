import json
from collections import defaultdict

from run_experiments.utils import get_last_token_prob

with open("run_experiments/models.json", "r") as f:
    models = json.load(f)

with open("data/prompts.json", encoding="utf-8") as f:
    prompts = json.load(f)


# test experiment with no profiles and hearts
def main():

    get_last_token_prob("answer A", models["vllm"]["qwen3"])

    out = []

    trial_data =  prompts["no_profiles_hearts"]

    system_message = trial_data["system_message"]
    for trial_items in trial_data["trial_items"]:

        prompt = f"{system_message}\n\n{trial_items['prompt']}"
        metadata = trial_items["metadata"]

        pass


if __name__ == "__main__":
    main()