#Main class.
from Discovery import *
from RestService import *
class Provisioner:

#    if __name__ == '__main__':
    discovery = Discovery()
    devices = discovery.getDevices()
    print(devices[0].connection.info())
        #Discover devices and what they're currently doing (Get facts and if services are already running).


    rest = RestService()

#Have a placeholder SDN input to get detailed location and context aware data? Should this not be done at the provisioner? It depends on what orchestrator it is attached to.
#Generate topology from devices available (update variables used for REST)


#Start RestService.py


