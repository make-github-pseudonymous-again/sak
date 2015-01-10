
import sys

MSG_NOT_VALID = "Please respond with 'yes' or 'no' (or 'y' or 'n')."
YES = "yes"
NO = "no"
VALID = {
	YES: True,
	"y": True,
	"ye": True,
	NO: False,
	"n": False
}

def yesorno(question, default = YES):
	"""Ask a yes/no question via raw_input() and return their answer.

	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is one of "yes" or "no".
	"""

	if default is None:
		prompt = " [y/n] "
	elif default == YES:
		prompt = " [Y/n] "
	elif default == NO:
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)

	while True:
		print(question + prompt, end = '')
		choice = input().lower()
		if default is not None and choice == '':
			return VALID[default]
		elif choice in VALID:
			return VALID[choice]
		else:
			print(MSG_NOT_VALID)
