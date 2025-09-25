import os
import json
from itertools import product

from generate.prompts.generate import generate_prompts


def main() -> None:

	out_folder = "data"
	os.makedirs(out_folder, exist_ok=True)

	out_data = {}
	# generate prompts with and without profiles, in plain and hearts mode
	for use_profiles, mode in product([True, False], ["plain", "hearts"]):

		output_file = os.path.join(out_folder, "prompts.json")

		data = generate_prompts(
			use_profiles=use_profiles,
			mode=mode
		)

		key = f"{'with' if use_profiles else 'no'}_profiles_{mode}"
		out_data[key] = data

	with open(output_file, "w", encoding="utf-8") as f:
		json.dump(out_data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
	main()