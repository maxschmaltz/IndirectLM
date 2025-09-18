import json

from run_experiments.speaker_experiment import trial

with open("run_experiments/models.json", "r") as f:
    models = json.load(f)

with open("data/prompts.json", encoding="utf-8") as f:
    prompts = json.load(f)


# test experiment with no profiles and hearts
def main():

    system_message = prompts["no_profiles_plain"][0]["system_message"]
    prompt_text = prompts["no_profiles_plain"][0]["trial_items"][0]["prompt"]
    prob_distr = trial(prompt_text, models["qwen3"])
    prob_distr


if __name__ == "__main__":
    main()