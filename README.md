## Setup

1. Install vLLM
```bash
pip install vllm
```

2. Serve the model as below. vLLM pulls the models from HF so the name should correspond to the path on HF.
```bash
vllm serve meta-llama/Llama-3.2-1B \
  --max-model-len 512 \
  --max-num-batched-tokens 512 \
  --port 8000 \
  --host 0.0.0.0
```