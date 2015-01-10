
import inspect

def pretty(o, linenos = False, filename = False):
	lines = []
	if filename : lines.append(inspect.getsourcefile(o) + "\n")
	if linenos :
		source, i = inspect.getsourcelines(o)
		n = len(source)
		w = len(str(n))
		for item in source :
			lines.append(str(i).rjust(w) + " " + item)
			i += 1
	else : lines.append(inspect.getsource(o))
	return "".join(lines)
