import os
from collections import defaultdict
import json
from itertools import product
import random
from typing import Literal, List, Optional, Tuple

from data.generate.templates import (
	TEMPLATE_VIGNETTE_PLAIN,
    TEMPLATE_VIGNETTE_HEARTS,
	PROFILE_TEMPLATE,
	HEARTS_HINT,
	PLAIN_HINT,
	SYSTEM_MESSAGE_TEMPLATE,
	PROMPT_TEMPLATE
)

with open("data/orig/vignette_elements.json") as f:
	_elements = json.load(f)

with open("data/orig/exp_2_speaker.json") as f:
	_exp_2_data = json.load(f)


def get_random_name(
	gender: Literal["male", "female"],
	used_names: List[str]
) -> str:
	name_pool = _elements["names"][gender]
	available_names = list(set(name_pool) - set(used_names))
	if not available_names:
		# unique names exhausted, allow reuse
		used_names = [used_names[-1]]	# keep the last used name to avoid immediate reuse
	return random.choice(list(set(name_pool) - set(used_names)))


def opinion2text(
	opinion: int,
	mode: Literal["plain", "hearts"]
) -> str:
	if mode == "plain":
		return _elements["expressions"][str(opinion)][0]
	else:
		return ("❤️ " * opinion + "♡ " * (5 - opinion)).strip()
	

def build_vignette(
	*,
	topic: str,
	opinion_a: int,
	opinion_b: int,
	name_a: Optional[str]=None,
	# name_b: Optional[str]=None, # never given
	goal: Literal["informational", "social", "mixed"],
	adjectives: List[str],
	mode: Literal["plain", "hearts"],
	used_names: Optional[List[str]]=[]
) -> str:
	
	if not name_a:
		# names are generated on demand
		gender_a = random.choice(["male", "female"])
		name_a = get_random_name(gender_a, used_names=used_names)
	else:
		gender_a = "female" if name_a in _elements["names"]["female"] else "male"
	pron_nom, pron_poss = ("she", "her") if gender_a == "female" else ("he", "his")

	gender_b = random.choice(["male", "female"])
	name_b = get_random_name(gender_b, used_names=used_names + [name_a])
		
	used_names.extend([name_a, name_b])

	# first, format the conversational goal as it includes additional placeholders
	behavior = _elements["conversations"][goal].format(pron_poss=pron_poss)

	# get the text from topic
	topic_extended = _elements["topics"][topic]

	# get opinions as heart visualizations
	hearts_a = opinion2text(opinion_a, mode=mode)
	hearts_b = opinion2text(opinion_b, mode=mode)

	# generate options
	options = ""
	for id, adjective in zip(["A", "B", "C", "D", "E"], adjectives):
		options += f"{id}: {topic_extended} {adjective}.\n"

	template = TEMPLATE_VIGNETTE_PLAIN if mode == "plain" else TEMPLATE_VIGNETTE_HEARTS

	# build the vignette
	vignette = template.format(
		name_a=name_a,
		topic=topic,
		name_b=name_b,		
		hearts_a=hearts_a,
		pron_nom=pron_nom,
		hearts_b=hearts_b,
		conversational_goal=behavior,
		options=options
	)

	return vignette


def reconstruct_experiment(
	*,
	experiment_info: str,
	mode: Literal["plain", "hearts"]="plain"
) -> Tuple[str, List[dict]]:
	
	used_names = []
	
	profile = PROFILE_TEMPLATE.format(
		age=experiment_info["age"],
		gender=experiment_info["gender"]
	)
	
	opinion_hint = HEARTS_HINT if mode == "hearts" else PLAIN_HINT
	system_message = SYSTEM_MESSAGE_TEMPLATE.format(
		profile=profile,
		opinion_hint=opinion_hint
	)

	trial_items = []
	for trial in experiment_info["trials"]:

		used_names.extend([trial["name_a"]])

		vignette = build_vignette(
			topic=trial["topic"],
			opinion_a=trial["opinion_a"],
			opinion_b=trial["opinion_b"],
			name_a=trial["name_a"],
			goal=trial["goal"],
			adjectives=trial["adjectives"],
			mode=mode,
			used_names=used_names
		)
		
		prompt = PROMPT_TEMPLATE.format(
			opinion_hint=opinion_hint,
			vignette=vignette
		)

		trial_items.append({
			"prompt": prompt,
			"metadata": {
				"match": trial["opinion_a"] == trial["opinion_b"],
				"conversational_goal": trial["goal"],
				"is_positive": trial["opinion_a"] == 5,
				"response": trial["response"]
			}
		})

	return system_message, trial_items


def synthesize_experiment(
	*,
	mode: Literal["plain", "hearts"]="plain"
) -> List[str]:
	
	used_names = []
	trial_items = []
	
	opinion_hint = HEARTS_HINT if mode == "hearts" else PLAIN_HINT
	system_message = SYSTEM_MESSAGE_TEMPLATE.format(opinion_hint=opinion_hint, profile="")

	topics = list(_elements["topics"].keys())
	random.shuffle(topics)

	# design parameters: 2 x 3 x 2
	param_space = [
		[True, False],  # match
		["informational", "social", "mixed"],  # conversational_goal
		[True, False],  # is_positive
		# if no profile, we want to explore the whole space with different topics
		# since we will run a single trial
		topics
	]

	for match, conversational_goal, is_positive, topic in product(*param_space):

		# factorize opinions
		opinion_a = 5 if is_positive else 1
		opinion_b = opinion_a if match else (5 - opinion_a) + 1

		adjectives = []
		for i in range(5):
			expression = random.choice(
				_elements["expressions"][str(i + 1)][1]
			)
			adjectives.append(expression)

		# build vignette
		vignette = build_vignette(
			topic=topic,
			opinion_a=opinion_a,
			opinion_b=opinion_b,
			goal=conversational_goal,
			adjectives=adjectives,
			mode=mode,
			used_names=used_names
		)
		
		prompt = PROMPT_TEMPLATE.format(
			opinion_hint=opinion_hint,
			vignette=vignette
		)
		trial_items.append({
			"prompt": prompt,
			"metadata": {
				"match": match,
				"conversational_goal": conversational_goal,
				"is_positive": is_positive
			}
		})

	return system_message, trial_items


def main() -> None:

	out_folder = "data/out"
	os.makedirs(out_folder, exist_ok=True)
	output_file = os.path.join(out_folder, "prompts.json")

	out_data = defaultdict(dict)
	# generate prompts with and without profiles, in plain and hearts mode
	for mode in ["plain", "hearts"]:

		# first, reconstruct real experiments
		real_experiment_items = []
		for experiment_info in _exp_2_data:
			system_message, trial_items = reconstruct_experiment(
				experiment_info=experiment_info,
				mode=mode
			)
			real_experiment_items.append({
				"system_message": system_message,
				"trial_items": trial_items
			})
		out_data["real"][mode] = real_experiment_items

		# then, synthesize new experiments
		system_message, trial_items = synthesize_experiment(mode=mode)
		out_data["synthetic"][mode] = [{
			"system_message": system_message,
			"trial_items": trial_items
		}]

	with open(output_file, "w", encoding="utf-8") as f:
		json.dump(out_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
	main()