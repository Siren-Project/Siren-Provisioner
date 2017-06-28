import logging
import threading
import json
from random import randint
import random

class Deployer:

    discovery = None
    def __init__(self, discovery, lifecycle_manager):
        self.discovery = discovery
        self.lifecycle_manager = lifecycle_manager

    #need to add container limitations
    def deploy_docker(self, node_id, image_name, port_bindings, ports=None):
        self.discovery.get_node(node_id).create_container(image_name, ports, port_bindings)
        #identifiy node from discovery information

    #agents are docker containers that persist after reboot.
    def deploy_agents(self, node_ids, image_name):
        service_id = randint(1, 1000000)
        for node_id in node_ids:
            logging.info("Provisioning agent to %s", node_id)
            threading.Thread(target=self.discovery.get_node(node_id).add_agent,
                         args=(image_name, 250, service_id)).start()

    def rand_provision(self):
        with open('nodes.json') as json_data:
            ips = json.load(json_data)['nodes']
        service_names = ['a', 'b', 'c']
        service_name = random.choice(service_names)
        self.deploy_dockers(ips, "lyndon160/service_"+service_name+"_video", {80: randint(50000, 64444)}, randint(5, 9) * 0.001,
                       ram=randint(10, 50), ports=[80])

    def deploy_dockers(self, node_ids, image_name, port_bindings, hours, ram=0, ports=None):
        logging.info(port_bindings)
        #need to register service here?
        service_id = randint(1, 1000000)

        for node_id in node_ids:
            logging.info("Provisioning to %s", node_id)
            #Threading this might be a bad idea
            if self.discovery.get_node(node_id):
                threading.Thread(target=self.discovery.get_node(node_id).create_container, args=(image_name, ports, port_bindings, ram, service_id)).start()
            #self.discovery.get_node(node_id).create_container(image_name, ports, port_bindings, ram, service_id)

        #only register service if deployment was successful?
        self.lifecycle_manager.register_service(node_ids, hours, service_id)
        return service_id
