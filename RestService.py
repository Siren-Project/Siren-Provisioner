from flask import Flask, url_for, request, Response
import json
import logging
from random import randint
class RestService:

#class RestService:


    app = Flask(__name__)

    deployer = None
    discovery = None
    @app.route('/')
    def api_root():
        return 'Read <a href="https://github.com/lyndon160/Siren-Provisioner"> https://github.com/lyndon160/Siren-Provisioner </a> for RESTful documentation'

    @app.route('/nodes', methods=['GET'])
    def api_nodes():
        #Get these from a database or at least a dynamic data list.
        #Data needs to include list of services
        # data = {
        #     'Nodes' : [
        #         {
        #             'Network': 10,
        #             'Location': 'Home',
        #             'Ownership': 'Residence owner',
        #             'Platform': 'ARM',
        #             'RAM': 500,
        #             'ID': 2,
        #             'Services' : [
        #                 {
        #                     'ID': 443634,
        #                     'RAM': 20,
        #                     'Bandwidth': 1
        #                  },
        #                 {
        #                     'ID': 1251,
        #                     'RAM': 200,
        #                     'Bandwidth': 5
        #                 }
        #             ]
        #         },
        #         {
        #             'Network': 10000,
        #             'Location': 'ISP core',
        #             'Ownership': 'BT',
        #             'Platform': 'ARM',
        #             'RAM': 10000,
        #             'ID': 2,
        #             'Services': [
        #                 {
        #                     'ID': 145634,
        #                     'RAM': 20,
        #                     'Bandwidth': 1
        #                 },
        #                 {
        #                     'ID': 14534,
        #                     'RAM': 200,
        #                     'Bandwidth': 5
        #                 },
        #                 {
        #                     'ID': 14535,
        #                     'RAM': 200,
        #                     'Bandwidth': 5
        #                 },
        #                 {
        #                     'ID': 14536,
        #                     'RAM': 200,
        #                     'Bandwidth': 5
        #                 },
        #                 {
        #                     'ID': 14537,
        #                     'RAM': 200,
        #                     'Bandwidth': 5
        #                 }
        #             ]
        #
        #         },
        #         {
        #             'Network': 1000,
        #             'Location': 'Telephone exchange',
        #             'Ownership': 'BT',
        #             'Platform': 'ARM',
        #             'RAM': 5000,
        #             'ID': 3,
        #             'Services': [
        #                 {
        #                     'ID': 125634,
        #                     'RAM': 20,
        #                     'Bandwidth': 1
        #                 },
        #                 {
        #                     'ID': 1451,
        #                     'RAM': 200,
        #                     'Bandwidth': 5
        #                 }
        #             ]
        #         }
        #     ]
        # }
        data = discovery.get_topology()
        resp = Response(json.dumps(data))
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return resp

    @app.route('/nodes/containers', methods=['GET'])
    def api_nodes_and_containers():
        data = discovery.get_topology_with_containers()
        resp = Response(json.dumps(data))
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return resp

    #    return 'List of ' + url_for('api_nodes')

    #Just a single node at the moment
#    @app.route('/nodes/<nodeid>/provision_docker', methods=['POST'])
#    def api_provision_docker(self, node_ids):
#        if not request.json or not 'image_name' in request.json:
#            pass
#        self.deployer.deploy_docker(0, request.json['image_name'])
       # return "Provisioned " + request.json['docker_name'] + " to " + nodeid
#        resp = Response(json.dumps({'image_name': request.json['image_name']}), status=200, mimetype='application/json')
#        return resp

    #image_name nodes ram hours
    @app.route('/nodes/provision_dockers', methods=['POST', 'GET'])
    def api_provision_dockers():
        logging.info(request.json)
        if not request.json or 'image_name' not in request.json or 'nodes' not in request.json or 'port_bindings' not in request.json or 'ram' not in request.json or 'hours' not in request.json:
            logging.warning("Missing infromation of provision %s", request.json)
            resp = Response("Error, did not include correct request information", status=400, mimetype='application/json')
            return resp
        # Randomized port binding to overcome service on same host problem
        random_external_port = randint(40000, 60000)
        #port_bindings= {request.json['port_bindings']['internal']:
        #    def deploy_dockers(self, node_ids, image_name, port_bindings, hours, ram=0, ports=None):

        #request.json['port_bindings']['external']}
        service_id = deployer.deploy_dockers(request.json['nodes'], request.json['image_name'], {request.json['port_bindings']['internal']: random_external_port}, request.json['hours'], request.json['ram'])
        resp = Response(json.dumps({'service_id': service_id, 'external_port': random_external_port}), status=200, mimetype='application/json')
        return resp

    @app.route('/nodes/<nodeid>')
    def api_node(self, nodeid):
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


    @app.route('/nodes/<nodeid>/containers')
    def api_node_containers(nodeid):
        # Change this to dynamically grab a node from database
        d = discovery.get_node(nodeid.replace("_", "."))
        data = {}
        if(d):
           data = d.get_running_containers()

        logging.info(data)

        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return resp


    @app.route('/nodes/<nodeid>/remove_service', methods=['PUT', 'GET'])
    def api_remove_service(nodeid):
        if request.method == 'GET':
            return "You need to use DELETE to remove a container\n"
        elif request.method == 'PUT':
            return "ECHO: PUT\n"
        elif request.method == 'DELETE':
            return "TODO. Delete container on node"

        return "TODO. Delete container on node"


    @app.route('/remove_service', methods=['DELETE'])
    def api_remove_service_by_id():
        if request.method == 'GET':
            return "You need to use DELETE to remove a container\n"
        elif request.method == 'DELETE':
            resp = Response(json.dumps({'service_id': request.json['service_id']}), status=200, mimetype='application/json')
            return  resp

        return "TODO. Delete container on node"

    #NEED TO REMOVE THREADS ABOUT SERVICE DELETION
    @app.route('/reset_all', methods=['GET'])
    def api_reset_all():
        for device in discovery.get_devices():
            device.wipe()

        resp = Response(json.dumps("Reset all"))
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')


        #Wipe lifecycle manager
        lifecycle.services={}

        return resp

    @app.route('/remove_all_images', methods=['DELETE'])
    def api_remove_all_images():
        for device in discovery.get_devices():
            device.wipe_images()
        return "Scenario reset"

   # if __name__ == '__main__':
   #     app.run(port=60000)




    def __init__(self, dep, dis, lif):
        global deployer, discovery, lifecycle
        deployer = dep
        discovery = dis
        lifecycle = lif
        self.app.use_reloader=False
        #self.app.debug = True
        self.app.run(host='0.0.0.0', port=60000, threaded=True)

