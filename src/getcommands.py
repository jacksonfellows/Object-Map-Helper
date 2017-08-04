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