def selection_form(data, target, name, radio=False, hidden=[]):
	body = ''
	for i in data:
		body += '<input value="{0}" name="{1}" type="{2}"> {0}</br>'.format(i, name, 'radio' if radio else 'checkbox')
	for i in hidden:
		body += '<input name="{0}" value="{1}" type="hidden">'.format(i[0], i[1])
	body += '</br><input type="submit" value="Submit">'
	return '<form method="post" action="{0}">{1}</form>'.format(target, body)