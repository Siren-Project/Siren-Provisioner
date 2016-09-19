from docker import Client
class Device:
    ip = ""
    connection = None
    info = None
    def __init__(self, ip):
        self.ip = ip
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

    #memory, lifespan? (this might be managed by the provisioner),
    def create_container(self, image, ports, port_bindings):
        self.connection.pull(image)

        container = self.connection.create_container(image=image, ports=ports,
                                                     host_config=self.connection.create_host_config(
                                                         port_bindings=port_bindings))
        #Create host config, this may overwrite previous config
        try:
            self.connection.start(container.get('Id'))
        except Exception as err:
            print('Error: Could not start container', err)
        return container


    def get_connection(self):
        return self.connection


