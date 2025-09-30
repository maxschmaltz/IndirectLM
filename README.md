# Investigating Indirect Communication Abilities of Transformer-based LMs

Geetansh Saxena & Maksim Shmalts. University of Tübingen

---

## Abstract

Human language understanding relies heavily not only on the linguistic meaning of the perceived language signs, but also on a large set of extra-linguistic notions, beliefs, immediate contextual cues, and much more. Many attempts have been made to build a model of human communication that would include these pragmatic factors. In particular, Achimova et al. (2025) suggest that the choice of the utterance is actively affected by the speaker’s belief about the listener’s opinion on the conversation topic and confirms this hypothesis with experiments with human participants. We aim at investigating to what extent this behavior is transmitted to language models (LMs). We report a noticeable correlation between the size of the model and the extent to which it acquires the investigated behavioral pattern. We find that smaller LMs are incapable of replicating the discussed indirect speech tendency, while larger models show some initial yet promising results in that direction.


## Technical Setup

Two following models were utilized for the experiments:

* [SmolLM-360M](https://huggingface.co/HuggingFaceTB/SmolLM-360M)
* [Llama3.2-1B](https://huggingface.co/meta-llama/Llama-3.2-1B)
* [SmolLM-1.7B-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM-1.7B-Instruct)
* [Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507)


The models were run locally via a vLLM server.

To reproduce the experiments, the following setup is required:

1. Pull the repository

```bash
git clone https://github.com/maxschmaltz/IndirectLM.git
```


1. Install requirements
```bash
pip install -r requirements.txt
```

2. Serve the desired as below. vLLM pulls the models from HF so the name should correspond to the path on HF. Here's an example for Llama3.2-1B:

```bash
vllm serve meta-llama/Llama-3.2-1B \
  --max-model-len 512 \
  --max-num-batched-tokens 512 \
  --port 8000 \
  --host 0.0.0.0
```


## Reproduce Experiments

### Speaker Experiment

To reproduce the Pragmatic Speaker Experiment, run the main function of [speaker_experiment.py](run_experiments/speaker_experiment/speaker_experiment.py) from the root of the repository:

```
import asyncio

from run_experiments import run_speaker_experiment

if __name__ == "__main__":
    asyncio.run(main())
```

Make sure to have set the `MODEL_NAME` constant in [utils.py](run_experiments/utils.py) identical to the model path served with vLLM.

The experiment will run 5-15 hours depending on the model. The results will be saved in the folder [data/out](data/out) under name `prompts_speaker_exp_<short_model_name>`.

### Pragmatic Listener Experiment
To reproduce the Pragmatic Listener Experiment, 

**Prerequisites (step 1 and 2)**: 

**Step 1**: run the vllm server with you favourable model 

**Step 2**: change the MODEL_NAME variable in exp_pragmatic_listener/run_experiment.py file with the model you are running on vllm. 

For example if you run 
```
vllm serve Qwen/Qwen3-4B-Instruct-2507 \
  --max-model-len 512 \
  --max-num-batched-tokens 512 \
  --port 8000 \
  --host 0.0.0.0
```

then the `MODEL_NAME` is 'Qwen/Qwen3-4B-Instruct-2507'. 

**Step 3**: run `python3 exp_pragmatic_listener/run_experiment.py` in another shell
