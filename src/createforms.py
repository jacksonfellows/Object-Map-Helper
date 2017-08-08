def selection_form(data, target, name, radio=False):
	body = ''
	for i in data:
		body += '<input value="{0}" name="{1}" type="{2}"> {0}</br>'.format(i, name, 'radio' if radio else 'checkbox')
	body += '</br><input type="submit" value="Submit">'
	return '<form method="post" action="{0}">{1}</form>'.format(target, body)

def text_form(data, target):
	req_body = ''
	body = ''
	for param, required in data.items():
		text = '{0}{1}</br><input name="{0}" type="text" class="input-xxlarge"></br>'.format(param, ' (required)' if required else '')
		if required:
			req_body += text
		else:
			body += text
	body += '</br><input type="submit" value="Submit">'
	return '<form method="post" action="{0}">{1}{2}</form>'.format(target, req_body, body)

def show_error(message):
	body = ''
	for line in message.split('\n'):
		if line == '':
			continue
		body += '{0}</br>'.format(line)
	return '<div class="alert alert-danger">{0}</div>'.format(body)