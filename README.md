## Setup

1. Install vLLM
```bash
pip install vllm
```

2. Serve the model as below. vLLM pulls the models from HF so the name should correspond to the path on HF.
```bash
vllm serve Qwen/Qwen3-8B \
  --max-model-len 4096 \
  --max-num-batched-tokens 4096 \
  --port 8000 \
  --host 0.0.0.0
```