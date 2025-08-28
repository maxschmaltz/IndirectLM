import json
from itertools import product
import random
from typing import Literal, List, Optional

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
	profile: Optional[str]="",
	mode: Literal["plain", "hearts"]="plain"
) -> List[str]:
	
	params = []
	# design parameters: 2 x 3 x 2
	for match, conversational_goal, is_positive in product(
		[True, False],  # match
		["informational", "social", "mixed"],  # conversational_goal
		[True, False]  # is_positive
	):
		params.append((match, conversational_goal, is_positive))

	opinion_hint = HEARTS_HINT if mode == "hearts" else PLAIN_HINT
	system_message = SYSTEM_MESSAGE_TEMPLATE.format(
		profile=profile,
		opinion_hint=opinion_hint
	)

	# we have to sample 10 items for each trial
	params = random.choices(params, k=10)
	random.shuffle(params)

	# shuffle topics (we have 10, one per items)
	topic_items = list(_elements["topics"].items())
	random.shuffle(topic_items)

	used_names = []
	trial_items = []
	for i, (match, conversational_goal, is_positive) in enumerate(params):

		# factorize opinions
		opinion_a = 5 if is_positive else 1
		opinion_b = opinion_a if match else (5 - opinion_a) + 1

		# build vignette
		vignette = build_vignette(
			topic_item=topic_items[i],
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
	mode: Literal["plain", "hearts"],
	output_file: str
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