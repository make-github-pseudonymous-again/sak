
def parse(argv, args, kwargs):

	key = ""
	isflag = False
	isvalue = False
	islist = False

	for p in argv:

		if len(p) > 1 and p[0] == '-' and not p[1].isdigit():
			isvalue = False
			isflag = False
			islist = False
			if p[1] == '-':
				p = p[2:]

				if len(p) == 0 : continue

				v = True
				if len(p) > 1 and p[:2] == "no" :
					v = False
					p = p[2:]

				kwargs[p] = v
				key = p
				isflag = True

			elif len(p) == 2:

				p = p[1:]
				
				kwargs[p] = v
				key = p
				isflag = True
			
			else:
				for i in range(1, len(p)) : kwargs[p[i]] = True
					
		else :
			if isflag :
				isflag = False
				isvalue = True
				kwargs[key] = p
			elif isvalue : 
				isvalue = False
				islist = True
				kwargs[key] = [kwargs[key], p]
			elif islist : kwargs[key].append(p);
			else : args.append(p)
		
	
	return args, kwargs