import requests

# running vLLM, make sure to have completed the setup steps in README.md
BASE_URL = "http://0.0.0.0:8000/v1"
MODEL_NAME = "Qwen/Qwen3-8B"


def get_last_token_prob(prompt_text: str) -> tuple[str, float]:
    
    # use the completions endpoint with logprobs to get token probabilities
    api_key = "not-required"
    url = f"{BASE_URL}/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": MODEL_NAME,    # pulls model from HF
        "prompt": prompt_text,
        "temperature": 0,
        "max_tokens": 1,    # we don't want to generate anything, set min
        "logprobs": 1,
        "echo": True        # echo back the prompt in the response
    }

    response = requests.post(url, headers=headers, json=payload)
    response = response.json()

    # -2 because the last token is the generated one
    # and we want the last token of the prompt
    last_token, last_token_logprob = list(response["choices"][0]["logprobs"]["top_logprobs"][-2].items())[0]
    last_token_prob = float(2 ** last_token_logprob)

    return last_token, last_token_prob