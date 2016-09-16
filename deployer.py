class deployer:
    discovery = None
    def __init__(self, discovery):
        self.discovery = discovery

    #need to add container limitations
    def deploy_docker(self, node_id, image_name):
        self.discovery.get_node(node_id).get_connection()
        #identifiy node from discovery information


    def deploy_dockers(self, node_ids, image_name):
        pass