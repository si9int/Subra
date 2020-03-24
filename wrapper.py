import os, subprocess, json

home = os.environ['HOME']

def read_config():
	config = open(home + '/.config/subfinder/config.yaml', 'r').read()
	return [home, config]

def save_config(data):
	with open(home + '/.config/subfinder/config.yaml', 'w') as config_file:
		config_file.write(data)

def run_subfinder(domain, args):
	open('./tmp/{}.lock'.format(domain), 'w').close()

	if args:
		command = 'subfinder -d {} -o ./tmp/{}.json -oJ -nW {}'.format(domain, domain, args).split()
	else:
		command = 'subfinder -d {} -o ./tmp/{}.json -oJ -nW'.format(domain, domain).split()

	p = subprocess.Popen(command, stdout=subprocess.PIPE)

	p.communicate()
	os.remove('./tmp/{}.lock'.format(domain))
def load_scans():
	scans = []
	filtered = []

	for (path, dirname, filename) in os.walk('./tmp'):
		scans.extend(filename)

	for i,s in enumerate(scans):
		if not s.endswith('.lock'):
			filtered.append(s.split('.json')[0])

	return filtered

def get_result(domain):
	result = []
	data = open('./tmp/{}.json'.format(domain), 'r').read().splitlines()

	for d in data:
		d = json.loads(d)
		result.append([d['host'], d['ip']])

	return result

def get_idle():
	idle = []

	for i in os.listdir('./tmp'):
		if i.endswith('.lock'):
			idle.append(i.split('.lock')[0])

	return idle

def delete_target(domain):
	os.remove('./tmp/{}.json'.format(domain))

def get_text(domain, type):
	text = ''
	data = open('./tmp/{}.json'.format(domain), 'r').read().splitlines()

	for d in data:
		d = json.loads(d)
		if type == 'sub':
			text = text + d['host'] + '\n'
		else:
			text = text + d['ip'] + '\n'
	return text
