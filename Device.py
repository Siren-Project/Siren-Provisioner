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
        self.create_connection()
        self.info = self.get_info()
        self.reserved_memory = 0
        self.total_memory = None
        self.arch = None
        self.location = None
        if self.info:
            if 'raspberrypi' in self.info['Name']:
                self.location = "residence"
            self.total_memory = self.info['MemTotal']
            self.arch = self.info['Architecture']
            logging.info("Device memory: %sMB, location: %s, architecture: %s ", self.total_memory / 1024 / 1024,
                         self.location, self.arch)
        else:
            logging.warning("Device not initialised correctly")

        self.service_id_to_container_id = {}


        #
        # self.location =

    def create_connection(self):
        try:
            self.connection = Client(base_url='tcp://'+self.ip+":64243")
            self.info = self.connection.info()
        except Exception as err:
            logging.warning('Error: Could not start container on node %s with ip %s because: %s', self.id, self.ip, err)
    def get_id(self):
        return self.id
    def get_total_memory(self):
        return self.total_memory
    def get_arch(self):
        return self.arch
    def get_reserved_memory(self):
        return self.reserved_memory
    def get_location(self):
        return self.location
    def get_cpu(self):
        pass
    def get_info(self):
        try:
            return self.connection.info()
        except Exception as err:
            logging.warning('Error: Could not get info on node %s with ip %s because: %s', self.id, self.ip, err)
            return None
    def get_id(self):
        return self.id

    #Accepts ram in MegaBytes
    def create_container(self, image, ports, port_bindings, ram, service_id):
        container=None
        try:
            try:
                #This could be a problem if not image
                self.connection.pull(image)
            except Exception as err:
                logging.warning('Error: Could not pull image %s with ip %s because: %s. Trying to use anyway', self.id, self.ip, err)

            container = self.connection.create_container(image=image, ports=ports,
                                                         host_config=self.connection.create_host_config(
                                                             port_bindings=port_bindings, mem_limit=str(ram)+"m"))
            #Create host config, this may overwrite previous config

            self.connection.start(container.get('Id'))
            self.service_id_to_container_id[service_id] = container.get('Id')
            logging.info("Successfully ran container on %s", self.ip)

            self.reserved_memory += int(ram)

        except Exception as err:
            logging.warning('Error: Could not start container on node %s with ip %s because: %s', self.id, self.ip, err)
        logging.info("Services on this node %s", self.service_id_to_container_id)
        return container


    def wipe_images(self):
        try:
            images = self.get_image_ids()
            for i in images:
                self.remove_image(i)
        except Exception as err:
            logging.warning('Error: Removing image %s', err)


    def wipe(self):
        try:
            containers = self.get_container_ids()
            images = self.get_image_ids()
            self.reserved_memory = 0


            for c in containers:
                try:
                    self.remove_container(c)
                #    self.stop_container(c)
                #    self.kill_container(c)


                except Exception as err:
                    logging.warning('Error: Wiping container %s', err)
            #for i in images:
            #    self.remove_image(i)
        except Exception as err:
            logging.warning('Error: Wiping container %s', err)

    def get_container_ids(self):
        ids = []

        try:
            containers = self.connection.containers(all=True)
            for container in containers:
                ids.append(container['Id'])
        except Exception as err:
            logging.warning('Error: getting container %s', err)
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
        try:
            self.connection.remove_container(container_id, force=True)
        except Exception as err:
            logging.warning('Error: Could not remove container on node %s with ip %s because: %s', self.id, self.ip, err)
    def remove_image(self, image_name):
        self.connection.remove_image(image_name, force=True)

    def get_connection(self):
        return self.connection

    def get_container_ids_from_service_id(self, service_id):
        return self.service_id_to_container_id[service_id]

    #This returns a list of container objects that includes container id, image name.
    def get_running_containers(self):
        c = {}
        try:
            c = self.connection.containers()
        except Exception as err:
            logging.warning('Error: Could not get data on node %s with ip %s because: %s', self.id, self.ip, err)
        return c

    def get_running_image_names(self):
        pass

    def terminate_service(self, service_id):
        logging.info("Terminating service %s on node %s with IP %s", service_id, self.id, self.ip)
        try:
            self.remove_container(self.service_id_to_container_id[service_id])
        except Exception as err:
            logging.warning('Error: Could not terminate service on node %s with ip %s because: %s', self.id, self.ip, err)