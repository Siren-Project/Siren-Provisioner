from flask import Flask, url_for, request, Response
import json
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/nodes', methods = ['GET'])
def api_nodes():
    data = {
        'Nodes' : [1,2,3,4,5]
            }

    resp = Response(json.dumps(data))

    return 'List of ' + url_for('api_nodes')


@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"
    elif request.method == 'POST':
        return "ECHO: POST\n"
    elif request.method == 'PATCH':
        return "ECHO: PATCH\n"
    elif request.method == 'PUT':
        return "ECHO: PUT\n"
    elif request.method == 'DELETE':
        return "ECHO: DELETE"


@app.route('/nodes/<nodeid>')
def api_node(nodeid):
    # Change this to dynamically grab a node from database
    data = {
        'Network': 10,
        'Ownership': 'Residence owner',
        'Platform': 'ARM',
        'RAM': 500,
        'id': nodeid
            }
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(port=60000);
