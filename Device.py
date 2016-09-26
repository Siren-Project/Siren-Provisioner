from docker import Client
import logging
class Device:
#    ip = ""
#    connection = None
#    info = None
#    id = None

    def __init__(self, ip, identifier):
        logging.info("Creating new device with IP %s", ip)
        self.ip = ip
        self.id = identifier
        self.create_connection();

    def create_connection(self):
        self.connection = Client(base_url='tcp://'+self.ip+":64243")
        self.info = self.connection.info()

    def get_ram(self):
        pass
    def get_cpu(self):
        pass
    def get_info(self):
        pass
    def get_id(self):
        return self.id

    #memory, lifespan? (this might be managed by the provisioner),
    def create_container(self, image, ports, port_bindings):
        self.connection.pull(image)

        container = self.connection.create_container(image=image, ports=ports,
                                                     host_config=self.connection.create_host_config(
                                                         port_bindings=port_bindings))
        #Create host config, this may overwrite previous config
        try:
            self.connection.start(container.get('Id'))
            logging.info("Successfully ran container on %s", self.ip)
        except Exception as err:
            logging.warning('Error: Could not start container on node %s with ip %s because: %s', self.id, self.ip, err)

        return container

    def wipe(self):
            containers = self.get_container_ids()
            images = self.get_image_ids()

            for c in containers:
                try:
                    self.remove_container(c)
                #    self.stop_container(c)
                #    self.kill_container(c)


                except Exception as err:
                    logging.warning('Error: Wiping container %s', err)
            for i in images:
                self.remove_image(i)

    def get_container_ids(self):
        containers = self.connection.containers(all=True)
        ids = []
        for container in containers:
            ids.append(container['Id'])
        return ids

    def get_image_ids(self):
        images = self.connection.images()
        ids = []
        for image in images:
            ids.append(image['Id'])
        return ids

    def stop_container(self, container_id):
        self.connection.stop(container_id)
        self.connection.delete()

    def kill_container(self, container_id):
        self.connection.kill(container_id)

    def remove_container(self, container_id):
        self.connection.remove_container(container_id, force=True)
        pass

    def remove_image(self, image_name):
        self.connection.remove_image(image_name, force=True)

    def get_connection(self):
        return self.connection


