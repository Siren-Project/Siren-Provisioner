import logging
import threading
from random import randint
class Deployer:

    discovery = None
    def __init__(self, discovery, lifecycle_manager):
        self.discovery = discovery
        self.lifecycle_manager = lifecycle_manager

    #need to add container limitations
    def deploy_docker(self, node_id, image_name, port_bindings, ports=None):
        self.discovery.get_node(node_id).create_container(image_name, ports, port_bindings)
        #identifiy node from discovery information


    def deploy_dockers(self, node_ids, image_name, port_bindings, hours, ram=0, ports=None):
        #logging.info(node_ids, image_name, port_bindings, ram, hours)
        #need to register service here?
        service_id = randint(1, 1000000)

        for node_id in node_ids:
            logging.info("Provisioning to %s", node_id)
            #Threading this might be a bad idea
            threading.Thread(target=self.discovery.get_node(node_id).create_container, args=(image_name, ports, port_bindings, ram, service_id)).start()
            #self.discovery.get_node(node_id).create_container(image_name, ports, port_bindings, ram, service_id)
        self.lifecycle_manager.register_service(node_ids, hours, service_id)
        return service_id
