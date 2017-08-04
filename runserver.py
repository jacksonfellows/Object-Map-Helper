import json

from flask import Flask, request, render_template, jsonify

from src.jsonselector import codify_json
from src.flaskhelpers import extract_post_data

from src.updatemap import update_map

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/process', methods=['POST'])
def process():
    required_fields = ('raw_json',)
    post,errors = extract_post_data(request, required_fields)

    if errors:
        return jsonify(errors=errors)

    try:
        data = json.loads(post['raw_json'])
    except ValueError:
        return 'Invalid JSON'

    try:
        codified_json, region_path = codify_json(json.dumps(data))
    except ValueError, e:
        print(str(e))
        return 'Error'

    return render_template('codify_json.html', codified_json=codified_json, region_path=region_path)

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
