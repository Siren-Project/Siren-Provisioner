from Device import *
import threading
import json
import logging
import requests


class Discovery:

    """Discovery is a service that discovers new devices. This communicates with a separate discovery server."""

    with open('nodes.json') as json_data:
        data = json.load(json_data)
        ips = data['nodes']
        ips_location = data['nodes_locations']
    devices = [] #Should probably be a dictionary where device id is the key

    def __init__(self):
        self.discover_devices()
        # TODO this service should be a separate thread and should periodically discover_devices

    def connect_and_discover(self):
        result = requests.get("http://188.166.155.90:61112/nodes")
        print "Nodes from discovery server :" +str(result.json())
        return result.json()

    def discover_devices(self):
        online_nodes = self.connect_and_discover()
        for node in online_nodes:
            #if we have not already found it through config then add it
            if(not node['remote_ip'] in self.ips):
                print node['remote_ip']
                self.ips.append(node['remote_ip'])
            #Make into set

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
        logging.warning("Device not found")

    def get_topology(self):
        topology = []
        for device in self.devices:
            topology.append({'id': device.get_id(), 'available_memory': (device.get_total_memory() / 1024 / 1024) - device.get_reserved_memory(), 'total_memory': device.get_total_memory()/1024/1024, 'reserved_memory': device.get_reserved_memory(), 'arch': device.get_arch(), 'location': device.get_location()})
        return topology


    def get_topology_with_containers(self):
        topology = []
        for device in self.devices:
            topology.append(
                {'id': device.get_id(), 'available_memory': (device.get_total_memory() / 1024 / 1024) - device.get_reserved_memory(),
                 'total_memory': device.get_total_memory() / 1024 / 1024, 'reserved_memory': device.get_reserved_memory(),
                 'arch': device.get_arch(), 'location': device.get_location(), 'containers': device.get_running_containers()})
        return topology