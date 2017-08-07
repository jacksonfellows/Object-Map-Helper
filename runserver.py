import json

from flask import Flask, request, render_template, jsonify

from src.jsonselector import codify_json, get_info
from src.updatemap import update_map
from src.parseawshelp import get_commands
from src.createforms import selection_form

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    commands = get_commands('aws')
    return render_template('form.html', form=selection_form(commands, '/actions', 'service'), message='Choose a service to add to the object id map:')

@app.route('/testing', methods=['GET'])
def testing():
    return render_template('home.html')

@app.route('/actions', methods=['POST'])
def actions():
    service = request.form['service']

    commands = get_commands('aws '+service)
    return render_template('form.html', form=selection_form(commands, '/commands'), message='Select actions to add to the object id map:')

@app.route('/process', methods=['POST'])
def process():
    try:
        data = json.loads(request.form['raw_json'])
    except ValueError:
        return 'Invalid JSON'

    codified_json, region_path = codify_json(json.dumps(data))
    service, action = get_info(data)

    return render_template('codify_json.html', codified_json=codified_json, region_path=region_path, service=service, action=action)

@app.route('/create_map', methods=['POST'])
def create_map():
    id_path = request.form['selector']
    region_path = request.form['region']
    service = request.form['service']
    action = request.form['action']

    new_map = update_map(id_path, region_path, service, action)
    map_json, region_path = codify_json(new_map)

    return render_template('show_map.html', map_json=map_json)

@app.route('/objectidmap', methods=['GET'])
def objectidmap():
    with open('objectidmap.json') as rawjson:
        return rawjson.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
