import os, re

def get_commands(base):
	os.system(base+' help > commands')
	with open('commands') as fl:
		commands = [[]]
		words = re.split('[\s]+', fl.read())
		j = 0
		for i in range(len(words)):
			if words[i-1] == '+\x08o':
				commands[j].append(words[i])
				if i+1 < len(words) and words[i+1] != '+\x08o':
					j += 1
					commands.append([])

	os.remove('commands')

	return max(commands, key=lambda a: len(a))

def try_command(command):
	exit = os.system(command+' &> errors')
	res = True
	if exit != 0:
		with open('errors') as fl:
			res = fl.read()
	os.remove('errors')
	return res

def get_params(command):
	os.system(command+' help > params')
	with open('params') as fl:
		params = {}
		words = re.split('[\s]+', fl.read())
		for i in range(len(words)):
			if '<value>' in words[i]:
				param = words[i-1]
				if param[0] == '[':
					params[param[1:]] = False
				else:
					params[param] = True
	os.remove('params')
	return params