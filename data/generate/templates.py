TEMPLATE_VIGNETTE_PLAIN = """\
{name_a} wants to discuss {topic} with {name_b}.
{name_a} feels {hearts_a} about the issue.
{name_a} thinks that {name_b} feels {hearts_b} about it, but {pron_nom} is not sure.

{name_a} {conversational_goal} \
What would {name_a} say?

{options}\
"""


TEMPLATE_VIGNETTE_HEARTS = """\
{name_a} wants to discuss {topic} with {name_b}.

Here's how {name_a} feels about the issue: \
Strongly negative	{hearts_a}	Strongly positive

{name_a} thinks this is how {name_b} feels about it, but {pron_nom} is not sure: \
Strongly negative	{hearts_b}	Strongly positive

{name_a} {conversational_goal} \
What would {name_a} say?

{options}\
"""


PROFILE_TEMPLATE = "a {age} years old {gender} US-English speaker "


HEARTS_HINT = """\
Hint: The opinions will be shown as hearts, \
where more full hearts ❤️ indicate more positive opinion. \
For example, "❤️ ❤️ ♡ ♡ ♡" means a somewhat negative opinion, \
while "❤️ ❤️ ❤️ ❤️ ❤️" means strongly positive opinion. \
"""


PLAIN_HINT = """\
Hint: The opinions will be written in a plain text, \
from "strongly negative" to "strongly positive". \
"""


SYSTEM_MESSAGE_TEMPLATE = """\
You are {profile}participating in a linguistic experiment. \
In the experiment, small dialogues of two persons on a certain topic will be given to you. \
The persons' opinions on the topic will also be shown to you, \
they may both match or mismatch. {opinion_hint}

You task is to pick the most natural utterance of the first person.
"""



PROMPT_TEMPLATE = """\
{opinion_hint}

Start!
===========================

{vignette}

===========================


Your answer is \
"""