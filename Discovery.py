from Device import *

#Service that discovers new devices. In future work this will be split out into a separate server.
class Discovery:
    ips = ['148.88.227.179', '148.88.227.232'] # read from file
    devices = [] #Should probably be a dictionary where device id is the key

    def __init__(self):
        self.discover_devices()
        #this service should be a separate thread and should periodically discover_devices


    def discover_devices(self):
        for ip in self.ips:
            self.devices.append(Device(ip))

    def get_devices(self):
        return self.devices

    def get_node(self, node_id):
        if self.devices:
            return self.devices[0]

