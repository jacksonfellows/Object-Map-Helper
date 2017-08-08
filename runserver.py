import json, time

from flask import Flask, request, render_template, jsonify

from src.jsonselector import codify_json, get_info
from src.updatemap import update_map
from src.parseawshelp import get_commands, try_command, get_params
from src.createforms import selection_form, text_form, show_error

service = ''
commands_list = []
c_i = 0
attempt = True
j_i = 0

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

    with open('proxy.json', 'w') as fl:
        json.dump([], fl)
    j_i = 0

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
    global j_i
    while True:
        time.sleep(1)
        with open('proxy.json') as fl:
            data = json.load(fl)
        if len(data) > j_i:
            break

    data = data[j_i]

    html_map, region_path = codify_json(json.dumps(data))
    service, warning, action = get_info(data)

    return render_template('edit_map.html', html_map=html_map, region_path=region_path, service=service, action=action, warning=show_error('Please correct capitilization of the service name') if warning else '', readonly='' if warning else 'readonly')

@app.route('/createmap', methods=['POST'])
def createmap():
    global j_i
    id_path = request.form['selector']
    region_path = request.form['region']
    service = request.form['service']
    action = request.form['action']

    new_map = update_map(id_path, region_path, service, action)
    map_json, region_path = codify_json(new_map)

    j_i += 1
    with open('proxy.json') as fl:
        if j_i == len(json.load(fl)):
            return render_template('show_map.html', map_json=map_json)
    return editmap()

@app.route('/proxy', methods=['POST'])
def proxy():
    new_json = json.loads(request.form['json'])
    with open('proxy.json') as fl:
        data = json.load(fl)
        data.append(new_json)
    with open('proxy.json', 'w') as fl:
        json.dump(data, fl)
    return 'ok'

@app.route('/objectidmap', methods=['GET'])
def objectidmap():
    with open('objectidmap.json') as rawjson:
        return rawjson.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)