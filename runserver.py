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
        codified_json = codify_json(json.dumps(data))
    except ValueError, e:
        print(str(e))
        return 'Error'

    return render_template('codify_json.html', codified_json=codified_json, target='unique id')

@app.route('/create_map', methods=['POST'])
def create_map():
    path = request.form['selector']
    service = request.form['service']
    action = request.form['action']

    new_map = update_map(path, service, action)

    return render_template('show_map.html', map_json=codify_json(new_map))

@app.route('/objectidmap', methods=['GET'])
def objectidmap():
    with open('objectidmap.json') as rawjson:
        return rawjson.read()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
