import json
import random
from typing import Literal, Tuple, List, Optional

with open("generate_experiments/vignettes/template_plain.txt") as f:
	_template_plain = f.read()

with open("generate_experiments/vignettes/template_hearts.txt") as f:
	_template_hearts = f.read()

with open("generate_experiments/vignettes/elements.json") as f:
	_elements = json.load(f)


def get_random_name(
	gender: Literal["male", "female"],
	used_names: Optional[List[str]] = []
) -> str:
	name_pool = _elements["names"][gender]
	return random.choice(list(set(name_pool) - set(used_names)))


def get_opinion(
	opinion: int,
	mode: Literal["plain", "hearts"] = "plain"
) -> str:
	if mode == "plain":
		return _elements["expressions"][str(opinion)][0]
	else:
		return ("❤️ " * opinion + "♡ " * (5 - opinion)).strip()
	

def build_vignette(
	*,
	topic_item: Tuple[str, str],
	opinion_a: int,
	opinion_b: int,
	goal: Literal["informational", "social", "mixed"],
	mode: Literal["plain", "hearts"] = "plain",
	used_names: Optional[List[str]] = []
) -> str:
	
	# names are generated on demand
	gender_a = random.choice(["male", "female"])
	name_a = get_random_name(gender_a, used_names)
	pron_nom, pron_poss = ("she", "her") if gender_a == "female" else ("he", "his")

	gender_b = random.choice(["male", "female"])
	name_b = get_random_name(gender_b, used_names + [name_a])

	used_names.extend([name_a, name_b])

	# first, format the conversational goal as it includes additional placeholders
	conversational_goal = _elements["conversations"][goal].format(pron_poss=pron_poss)

	# unpack the topic item
	topic, topic_extended = topic_item

	# get opinions as heart visualizations
	hearts_a = get_opinion(opinion_a, mode=mode)
	hearts_b = get_opinion(opinion_b, mode=mode)

	# generate options
	options = ""
	for i, id in enumerate(["A", "B", "C", "D", "E"]):
		expression = random.choice(
			_elements["expressions"][str(i + 1)][1]
		)
		options += f"{id}: {topic_extended} {expression}.\n"

	template = _template_plain if mode == "plain" else _template_hearts

	# build the vignette
	vignette = template.format(
		name_a=name_a,
		topic=topic,
		name_b=name_b,		
		hearts_a=hearts_a,
		pron_nom=pron_nom,
		hearts_b=hearts_b,
		conversational_goal=conversational_goal,
		options=options
	)

	return vignette