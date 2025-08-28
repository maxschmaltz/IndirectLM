import os
import requests
import dotenv

dotenv.load_dotenv()    # that loads the .env file variables into os.environ


# BASE_URL = "https://integrate.api.nvidia.com/v1"
BASE_URL = "https://api.openai.com/v1"


def get_last_token_prob(
    prompt_text: str,
    model_name: str
) -> tuple[str, float]:
    
    # use the completions endpoint with logprobs to get token probabilities
    # We set max_tokens=0 to avoid generating new tokens
    api_key = os.environ.get("OPENAI_API_KEY")
    url = f"{BASE_URL}/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    # # this payload is for the /chat/completions endpoint
    # # that does not return the logprobs for the prompt tokens
    # # so we utilize the older /completions endpoint instead
    # payload = {
    #     "model": model_name,
    #     "messages": [{"role": "user", "content": prompt_text}],
    #     "temperature": 0,
    #     "max_tokens": 1,    # we don't want to generate anything, set min
    #     "logprobs": True,
    #     "top_logprobs": 1,  # get logprobs for the prompt tokens
    #     "echo": True        # echo back the prompt in the response
    # }
    payload = {
        "model": model_name,
        "prompt": prompt_text,
        "temperature": 0,
        "max_tokens": 1,    # we don't want to generate anything, set min
        "logprobs": 1,
        "echo": True        # echo back the prompt in the response
    }
    response = requests.post(url, headers=headers, json=payload)
    response = response.json()

    last_token, last_token_logprob = list(response["choices"][0]["logprobs"]["top_logprobs"][-1].items())[0]
    last_token_prob = float(2 ** last_token_logprob)

    return last_token, last_token_prob