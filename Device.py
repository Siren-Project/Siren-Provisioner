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

    def get_cpu(self):

    def get_info(self):


