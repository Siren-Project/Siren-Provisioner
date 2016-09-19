class Deployer:
    discovery = None
    def __init__(self, discovery):
        self.discovery = discovery

    #need to add container limitations
    def deploy_docker(self, node_id, image_name, port_bindings, ports=None, ):
            self.discovery.get_node(node_id).create_container(image_name, ports, port_bindings)
        #identifiy node from discovery information


    def deploy_dockers(self, node_ids, image_name):
        pass