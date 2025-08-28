import json
from itertools import product
import random
from typing import Literal, List

from generate_experiments.vignettes.generate import build_vignette, _elements
from generate_experiments.templates import (
	PROFILE_TEMPLATE,
	HEARTS_HINT,
	PLAIN_HINT,
	SYSTEM_MESSAGE_TEMPLATE,
	PROMPT_TEMPLATE
)


def build_trial(
	*,
	profile: str,
	mode: Literal["plain", "hearts"]="plain"
) -> List[str]:
	
	used_names = []
	trial_items = []
	
	opinion_hint = HEARTS_HINT if mode == "hearts" else PLAIN_HINT
	system_message = SYSTEM_MESSAGE_TEMPLATE.format(
		profile=profile,
		opinion_hint=opinion_hint
	)

	topic_items = list(_elements["topics"].items())
	random.shuffle(topic_items)

	# design parameters: 2 x 3 x 2
	param_space = [
		[True, False],  # match
		["informational", "social", "mixed"],  # conversational_goal
		[True, False]  # is_positive
	]

	# if no profile, we want to explore the whole space with different topics
	# since we will run a single trial
	param_space.append(topic_items if profile == "" else [None])
		
	# sample 10 items for each trial if using profiles (following the original design)
	drop_indices = random.sample(range(12), k=2) if profile else []
	for i, (match, conversational_goal, is_positive, topic_item) in enumerate(product(*param_space)):

		if i in drop_indices:
			topic_items.insert(i, None)	# make indices match
			continue
		if not topic_item:
			topic_item = topic_items[i]

		# factorize opinions
		opinion_a = 5 if is_positive else 1
		opinion_b = opinion_a if match else (5 - opinion_a) + 1

		# build vignette
		vignette = build_vignette(
			topic_item=topic_item,
			opinion_a=opinion_a,
			opinion_b=opinion_b,
			goal=conversational_goal,
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


def generate_prompts(
	*,
	use_profiles: bool,
	mode: Literal["plain", "hearts"]
) -> None:
	
	if use_profiles:
		# 97 profiles downloaded from https://osf.io/nvrh9?view_only=86a0546483354ef49ad37c58e2cb4f0f
		# since answers from 6 participants were excluded and we don't know which ones,
		# we excluded 6 random profiles
		with open("generate_experiments/prompts/profiles.json") as f:
			_profiles = json.load(f)
			profiles = [
				PROFILE_TEMPLATE.format(
					age=profile[0],
					gender=profile[1]
				)
				for profile in _profiles
			]
		random.shuffle(profiles)
	else:
		profiles = [""]

	out_data = []
	for profile in profiles:
		system_message, trial_items = build_trial(
			profile=profile,
			mode=mode
		)
		out_data.append({
			"system_message": system_message,
			"trial_items": trial_items
		})

	return out_data