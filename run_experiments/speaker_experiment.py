import numpy as np

from run_experiments.utils import get_last_token_prob


def trial(
    prompt_text: str,
    model_name: str
) -> tuple[str, float]:
    
    target_probs = []
    for target in ["A", "B", "C", "D", "E"]:
        last_token, last_token_prob = get_last_token_prob(prompt_text + target, model_name)
        if last_token.strip() != target:
            target_probs.append(0)
        else:
            target_probs.append(last_token_prob)

    target_probs = np.array(target_probs)

    prob_distr = target_probs / target_probs.sum()
    return prob_distr