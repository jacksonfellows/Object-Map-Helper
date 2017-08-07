def box(value, name):
	if not name:
		name = value
	return '<input value="{0}" name="{1}" type="{2}"> {0}</br>'.format(value, name, 'checkbox' if name == value else 'radio')

def selection_form(data, target, name=None):
	body = ''
	for i in data:
		body += box(i, name)
	body += '</br><input type="submit" value="Submit">'
	return '<form method="post" action="{0}">{1}</form>'.format(target, body)