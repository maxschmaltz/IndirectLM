import json
import random
from typing import Literal, Tuple

with open("generate_experiments/template.txt") as f:
	_template = f.read()

with open("generate_experiments/vignette_elements.json") as f:
	_elements = json.load(f)


def get_random_person(gender: Literal["male", "female"]):
	return random.choice(_elements["names"][gender])


def visualize_opinion(opinion: int) -> str:
	return ("❤️ " * opinion + "♡ " * (5 - opinion)).strip()


def build_vignette(
	topic_item: Tuple[str, str],
	opinion_a: int,
	opinion_b: int,
	goal: Literal["informational", "social", "mixed"],
	target: Literal["A", "B", "C", "D", "E"]
) -> str:
	
	# names are generated on demand
	gender_a = random.choice(["male", "female"])
	name_a = get_random_person(gender_a)
	pron_nom, pron_poss = ("she", "her") if gender_a == "female" else ("he", "his")

	gender_b = random.choice(["male", "female"])
	name_b = get_random_person(gender_b)

	# ensure different names
	while name_a == name_b:
		name_b = get_random_person(gender_b)

	# first, format the conversational goal as it includes additional placeholders
	conversational_goal = _elements["conversations"][goal].format(pron_poss=pron_poss)

	# unpack the topic item
	topic, topic_extended = topic_item

	# get opinions as heart visualizations
	hearts_a = visualize_opinion(opinion_a)
	hearts_b = visualize_opinion(opinion_b)

	# generate options
	options = ""
	for i, id in enumerate(["A", "B", "C", "D", "E"]):
		expression = random.choice(
			_elements["expressions"][str(i + 1)]
		)
		options += f"{id}: {topic_extended} {expression}.\n"

	# build the vignette
	vignette = _template.format(
		name_a=name_a,
		topic=topic,
		name_b=name_b,		
		hearts_a=hearts_a,
		pron_nom=pron_nom,
		hearts_b=hearts_b,
		conversational_goal=conversational_goal,
		topic_extended=topic_extended,
		options=options,
		target=target
	)

	return vignette


if __name__ == "__main__":
	# example usage
	topic_item = random.choice(list(_elements["topics"].items()))
	opinion_a = random.choice([1, 5])
	opinion_b = random.choice([1, 5])
	goal = random.choice(["informational", "social", "mixed"])
	target = random.choice(["A", "B", "C", "D", "E"])

	vignette = build_vignette(topic_item, opinion_a, opinion_b, goal, target)
	print(vignette)