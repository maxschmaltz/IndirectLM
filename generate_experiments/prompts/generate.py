import numpy as np
from scipy.stats import skewnorm
from typing import Literal

with open("generate_experiments/prompts/template.txt") as f:
	_template = f.read()


# Since our LM(s) should be compared to human data, we need to prompt them to simulate
# the characteristics of the participants:
# 	Experiment 2 was designed to assess how the communicative goal, the actual opinion of the speaker,
# 	and an assumption about the listener’s belief affect utterance choices. We collected data
# 	from 98 US-English-speaking participants recruited via Prolific
# 	(45 female, 52 male, 1 person preferred not to report gender; age range 18–76, mean = 40, median = 35).
# 	Data from seven participants were excluded since they reported that they did not fully understand
# 	the instructions. Thus, data from 91 participants were entered into the analysis.
N_FEMALE = 45
N_MALE = 52
N_OTHER = 1
_n_participants = N_FEMALE + N_MALE + N_OTHER
_gender_p = [N_FEMALE / _n_participants, N_MALE / _n_participants, N_OTHER / _n_participants]
MIN_AGE = 18
MAX_AGE = 76
MEAN_AGE = 40
MEDIAN_AGE = 35
_age_skewness = MEAN_AGE - MEDIAN_AGE  # right tail is longer
_age_sd = 15  # rough estimate based on range, not reported in paper


def get_random_gender() -> Literal["male ", "female ", ""]:
	# TODO: later replicate with absolute numbers (45 female, 52 male, 1 other)?
	return np.random.choice(["male ", "female ", ""], p=_gender_p)


def get_random_age() -> int:
	age = skewnorm.rvs(a=_age_skewness, loc=MEAN_AGE, scale=_age_sd, size=1)[0]
    # clip to the allowed range
	return int(np.clip(age, MIN_AGE, MAX_AGE))


def get_prompt(
	gender: str,
	age: int,
	vignette: str,
	target: Literal["A", "B", "C", "D", "E"]
) -> str:
	prompt = _template.format(
		age=age,
		gender=gender,
		vignette=vignette,
		target=target
	)
	return prompt


if __name__ == "__main__":
	# test
	gender = get_random_gender()
	age = get_random_age()
	vignette = """\
Elizabeth wants to discuss immigration laws with Timothy.


Here's how Elizabeth feels about the issue:

Strongly negative       ❤️ ❤️ ❤️ ❤️ ❤️       Strongly positive


Elizabeth thinks this is how Timothy feels about it, but she is not sure:

Strongly negative       ❤️ ♡ ♡ ♡ ♡       Strongly positive


Elizabeth  wants to avoid possible conflicts.
What would Elizabeth say?

A: Our immigration laws are  awful.
B: Our immigration laws are  rather bad.
C: Our immigration laws are  okay.
D: Our immigration laws are  pretty good.
E: Our immigration laws are  amazing.

"""
	target = "D"

	prompt = get_prompt(
		gender=gender,
		age=age,
		vignette=vignette,
		target=target
	)
	print(prompt)