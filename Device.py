from docker import Client
import logging
import json
import time
from pprint import pprint
class Device:
#    ip = ""
#    connection = None
#    info = None
#    id = None
    connection_backoff=30

    def __init__(self, ip, identifier):
                logging.info("Creating new device with IP %s", ip)
                self.ip = ip
                self.id = identifier



                self.image_arch_modifier=""

                self.info = self.get_info()
                self.reserved_memory = 0
                self.total_memory = None
                self.arch = None
                self.location = None


                self.ips = []
                self.ips_location = []
                #Default port number

                self.port = "64243"

                with open('nodes.json') as json_data:
                    data = json.load(json_data)
                    self.ips = data['nodes']
                    self.ips_location = data['nodes_locations']
                devices = []  # Should probably be a dictionary where device id is the key

                # Change this to be read from config
                if (self.ip in self.ips):
                    for ip_location in self.ips_location:
                        if (ip_location["ip"] == self.ip):
                            #Configure this node
                            logging.info("Found location (%s) by ip (%s)", ip_location["location"], self.ip)
                            self.location = ip_location["location"]
                            if("tls" in ip_location):
                                if(ip_location["tls"]):
                                    self.tls=True
                            try:
                                if (ip_location["port"]):
                                    #logging.info("Adding port of %s", ip_location["port"])
                                    self.port = ip_location["port"]
                            except Exception as err:
                                logging.warning('Warning: Using default port (%s) because %s not defined', self.port, err)

                if (self.location == None):
                    logging.warning("Location not found for ip %s! Check nodes.json. Adding default of residence", self.ip)
                    self.location = "residence"


                self.create_connection()

                #TODO WARNING REMOVE THIS AFTER DEMO. WIPES DEVICES ON STARTUP
                self.wipe()


                if self.info:
                    self.total_memory = self.info['MemTotal']
                    self.arch = self.info['Architecture']

                    if(self.arch == "x86_64"):
                        self.image_arch_modifier = "_x86"


                    logging.info("Device memory: %sMB, location: %s, architecture: %s ", self.total_memory / 1024 / 1024,
                                 self.location, self.arch)
                else:
                    logging.warning("Device not initialised correctly")

                self.service_id_to_container_id = {}


    def create_connection(self):
        while(not self.info):
            try:
                #TODO add tls security. Will require local key.
                if hasattr(self, 'tls'):
                    if(self.tls):
                        logging.warning("Warning: TLS is not yet supported. No connection made to %s", self.ip)
                else:
                    self.tls = False

                if(not self.tls):
                    logging.info("Warning: TLS not enabled for node %s", self.ip)
                    self.connection = Client(base_url='tcp://'+self.ip+':'+self.port)
                self.info = self.connection.info()
            except Exception as err:
                logging.warning('Error: Could not connect to node %s with ip %s. Retrying in %s seconds. Error because: %s ', self.id, self.ip, Device.connection_backoff,  err)
                time.sleep(Device.connection_backoff)
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

    def add_agent(self, image, ram, service_id):

        container = None


        image += self.image_arch_modifier
        try:
            try:
                # This could be a problem if not image
                logging.info("Pulling %s", image)
                self.connection.pull(image)
            except Exception as err:
                logging.warning('Error: Could not pull image %s with ip %s because: %s. Trying to use anyway', self.id, self.ip,
                                err)

            container = self.connection.create_container(image=image,
                                                         host_config=self.connection.create_host_config(mem_limit=str(ram) + "m", restart_policy={"condition":"any"}))
            # Create host config, this may overwrite previous config

            self.connection.start(container.get('Id'))
            #self.service_id_to_container_id[service_id] = container.get('Id')
            logging.info("Successfully ran container on %s", self.ip)

            self.reserved_memory += int(ram)

        except Exception as err:
            logging.warning('Error: Could not start container on node %s with ip %s because: %s', self.id, self.ip, err)
        logging.info("Services on this node %s", self.service_id_to_container_id)
        return container

    #Accepts ram in MegaBytes
    def create_container(self, image, ports, port_bindings, ram, service_id):
        container=None

        image+=self.image_arch_modifier
        try:
            try:
                #This could be a problem if not image
                logging.info("Pulling %s", image)
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

    #Todo. Ignore images with agent in name
    def wipe_images(self):
        try:
            images = self.get_image_ids()
            for i in images:
                self.remove_image(i)
        except Exception as err:
            logging.warning('Error: Removing image %s', err)


    def wipe(self):
        logging.info("Wiping from %s", self.ip)
        try:
            containers = self.get_container_ids()
            images = self.get_image_ids()
            self.reserved_memory = 0


            for c in containers:
                try:
                    print c
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
                if(not "agent" in container['Image']):
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
        logging.info("Getting running containers of %s", self.id)
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