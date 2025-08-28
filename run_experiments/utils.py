import os
import requests
import dotenv

dotenv.load_dotenv()    # that loads the .env file variables into os.environ


# running Ollama, make sure to have completed the setup steps in README.md
# BASE_URL = "http://localhost:11434/v1"
BASE_URL = "http://localhost:8000/v1"


def get_last_token_prob(
    prompt_text: str,
    model_name: str
) -> tuple[str, float]:
    
    # use the completions endpoint with logprobs to get token probabilities
    # We set max_tokens=0 to avoid generating new tokens
    # api_key = "ollama"    # os.environ.get("OPENAI_API_KEY")
    url = f"{BASE_URL}/completions"
    headers = {
        "Content-Type": "application/json",
        # "Authorization": f"Bearer {api_key}"
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
    # this payload is for the /completions endpoint
    # that returns the logprobs for the prompt tokens
    # with OpenAI and vLLM but not with Ollama
    payload = {
        "model": model_name,    # pulls models from HF
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