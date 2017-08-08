import json

from flask import Flask, request, render_template, jsonify

from src.jsonselector import codify_json, get_info
from src.updatemap import update_map
from src.parseawshelp import get_commands, try_command, get_params
from src.createforms import selection_form, text_form, show_error

service = ''
commands_list = []
c_i = 0
attempt = True

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    commands = get_commands('aws')
    return render_template('form.html', form=selection_form(commands, '/actions', 'service', radio=True), message='Choose a service to add to the object id map:')

@app.route('/actions', methods=['POST'])
def actions():
    global service
    service = request.form['service']
    commands = get_commands('aws '+service)
    return render_template('form.html', form=selection_form(commands, '/commands', 'commands'), message='Select actions to add to the object id map:')

@app.route('/commands', methods=['POST'])
def commands():
    global commands_list, c_i
    commands_list = request.form.getlist('commands')
    c_i = 0
    attempt = True

    return command()

@app.route('/command', methods=['GET'])
def command():
    global service, commands_list, c_i, attempt
    c = commands_list[c_i]

    run = 'aws {0} {1}'.format(service, c)
    params = get_params(run)
    form = text_form(params, '/runcommand')
    if attempt != True:
        form = show_error(attempt) + form
    return render_template('form.html', form=form, message='Fill out the parameters for \'{0}\':'.format(run))

@app.route('/runcommand', methods=['POST'])
def runcommand():
    global service, commands_list, c_i, attempt
    c = commands_list[c_i]
    run = 'aws {0} {1}'.format(service, c)

    for tag, v in request.form.items():
        if v != '':
            run += ' {0} "{1}"'.format(tag, v)

    attempt = try_command(run)
    if attempt == True:
        c_i += 1
        if c_i == len(commands_list):
            return editmap()

    return command()

@app.route('/editmap', methods=['GET'])
def editmap():
    try:
        data = json.loads(request.form['raw_json'])
    except ValueError:
        return 'Invalid JSON'

    html_map, region_path = codify_json(json.dumps(data))
    service, action = get_info(data)

    return render_template('edit_map.html', html_map=html_map, region_path=region_path, service=service, action=action)

@app.route('/create_map', methods=['POST'])
def create_map():
    id_path = request.form['selector']
    region_path = request.form['region']
    service = request.form['service']
    action = request.form['action']

    new_map = update_map(id_path, region_path, service, action)
    map_json, region_path = codify_json(new_map)

    return render_template('show_map.html', map_json=map_json)

@app.route('/proxy', methods=['POST'])
def proxy():
    pass

@app.route('/objectidmap', methods=['GET'])
def objectidmap():
    with open('objectidmap.json') as rawjson:
        return rawjson.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)