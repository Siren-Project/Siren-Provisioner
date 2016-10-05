from Device import *
import threading
#Service that discovers new devices. In future work this will be split out into a separate server.
class Discovery:
    ips = ["192.168.2.13", "192.168.2.14", "192.168.2.15", "192.168.2.16", "192.168.2.17", "192.168.2.18"] # read from file
    devices = [] #Should probably be a dictionary where device id is the key

    def __init__(self):
        self.discover_devices()
        #this service should be a separate thread and should periodically discover_devices


    def discover_devices(self):
        for ip in self.ips:
            #We need to determine if device is discovered correctly. If not, periodically look for it.
            #Why might be not want to thread this? Device list could change.
            threading.Thread(target=self.discover_device, args=(ip, ip)).start()
            #d = Device(ip, ip)
            #if(d.info):
               # self.devices.append(d)

    def discover_device(self, ip, id):
        d = Device(ip, id)
        if (d.info):
            self.devices.append(d)

    def get_devices(self):
        return self.devices

    def get_node(self, node_id):
        if self.devices:
            for device in self.devices:
                if device.get_id() == node_id:
                    return device

    def get_topology(self):
        topology = []
        for device in self.devices:
            topology.append({'id': device.get_id(), 'available_memory': device.get_total_memory() - device.get_reserved_memory(), 'total_memory': device.get_total_memory(), 'reserved_memory': device.get_reserved_memory(), 'arch': device.get_arch(), 'location': device.get_location()})
        return topology
