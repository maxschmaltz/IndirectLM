import os
import json

with open("data/vignettes/elements.json") as f:
	_elements = json.load(f)


def main() -> None:

	# https://osf.io/nvrh9?view_only=86a0546483354ef49ad37c58e2cb4f0f
	input_folder = "data/exp_2_speaker"
	output_file = "data/exp_2_speaker.json"

	exp2_data = []
	for filename in os.listdir(input_folder):

		if filename.endswith(".txt"):

			file_path = os.path.join(input_folder, filename)
			with open(file_path, encoding="utf-8") as f:

				lines = json.load(f)	# a list of str

				# ignore first line ("topics")
				# get the topics for the 10 trials
				topics = lines[1:11]
				
				# ignore line 11 ("opinions")
				# get the opinions for the 10 trials
				opinions = lines[12:22]

				# ignore line 22 ("behaviour")
				# get the behaviours for the 10 trials
				behaviours = lines[23:33]

				# ignore line 33 ("adjectives")
				# get the adjectives for the 10 trials
				adjectives = lines[34:44]

				# ignore line 44 ("responses")
				# get the responses for the 10 trials
				responses = lines[45:55]

				# all the rest is subject info
				# we only need age and gender
				subject_info = lines[59]

				# finally build trials, combining the above info
				trials = []
				for topic, opinion, behaviour, adjective, response in zip(
					topics, opinions, behaviours, adjectives, responses
				):
					# mapping from the topic code to the text
					topic_extended = _elements["topics"][topic.strip()]
					# opinions are represented as a string of two comma-separated ints
					ind_oa, ind_ob = map(int, opinion.strip().split(","))
					# map the opinion ints to the corresponding adjectives
					opinion_a = adjective.split(",")[ind_oa - 1]
					opinion_b = adjective.split(",")[ind_ob - 1]
					# only the A's name is mentioned
					name_a = behaviour.split()[0]	
					trials.append({
						"topic": topic_extended,
						"opinion_a": opinion_a,
						"opinion_b": opinion_b,
						"name_a": name_a,
						"name_b": None,	# placeholder, will be filled in later
						"behaviour": behaviour.strip(),
						"response": response.strip()
					})
				# Build dictionary for this file
				# from subject info, we only need age and gender
				age = subject_info.split(",")[3]
				gender = subject_info.split(",")[4].lower()
				entry = {
					"age": age,
					"gender": gender,
					"trials": trials
				}
			
			exp2_data.append(entry)

	with open(output_file, "w", encoding="utf-8") as out_f:
		json.dump(exp2_data, out_f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
	main()