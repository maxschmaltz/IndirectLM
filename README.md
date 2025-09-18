## Setup
<!-- 
1. Install Ollama from https://ollama.com/download and run it

2. Go to the Terminal and pull the model:
```bash
ollama pull <model_name>
```

3. Run the model
```bash
ollama run <model_name>
``` -->


1. Install vLLM
```bash
pip install vllm
```

2. Serve the model as below. vLLM pulls the models from HF so the name should correspond to the path on HF.
```bash
vllm serve <HF_model_name> \
  --max-model-len 8192 \
  --max-num-batched-tokens 8192 \
  --port 8000 \
  --host 0.0.0.0
```