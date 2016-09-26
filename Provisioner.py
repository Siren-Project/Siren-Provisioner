#Main class.
from Discovery import *
from RestService import *
from Deployer import *
from LifecycleManager import *
import logging
class Provisioner:

        #Restores scenario to clean slate


        #Remove containers
        #Remove images
        #Wipe database of resources

    running = True
#    if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    discovery = Discovery()
    devices = discovery.get_devices()
  #  print(devices[0].connection.info())
  #  print(devices[1].connection.info())
    logging.info(devices[0].get_container_ids())
    deployer = Deployer(discovery)
    lifecycle_manager = LifecycleManager(discovery)
        #Discover devices and what they're currently doing (Get facts and if services are already running).
#    deployer.deploy_docker(0, "hypriot/armhf-hello-world")

    #deployer.deploy_docker(0, "hypriot/rpi-busybox-httpd", ports=[80], port_bindings={80: 64444})

    rest = RestService(deployer, discovery)


#Have a placeholder SDN input to get detailed location and context aware data? Should this not be done at the provisioner? It depends on what orchestrator it is attached to.
#Generate topology from devices available (update variables used for REST)
  #  while running:

