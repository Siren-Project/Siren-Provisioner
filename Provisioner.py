#Main class.
from Discovery import *
from RestService import *
from Deployer import *
from LifecycleManager import *
import logging
import threading

from random import randint

#from time import sleep
class Provisioner:

    def start_rest(deployer, discovery):
        rest = RestService(deployer, discovery)

    def rand_provision(deployer):
        deployer.deploy_dockers(["148.88.227.232", "148.88.227.179"], "hypriot/rpi-busybox-httpd", {80: randint(50000, 64444)}, randint(5, 9)*0.001,
                                ram=randint(10, 50), ports=[80])

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

    lifecycle_manager = LifecycleManager(discovery)
    deployer = Deployer(discovery, lifecycle_manager)
        #Discover devices and what they're currently doing (Get facts and if services are already running).
#    deployer.deploy_docker(0, "hypriot/armhf-hello-world")


    threading.Thread(target=start_rest, args=(deployer, discovery)).start()

    for i in [1,2,3,4,5,6]:
        threading.Thread(target=rand_provision, args=(deployer,)).start()

    #sleep(10)
    # deployer.deploy_dockers(["148.88.227.232", "148.88.227.179"], "hypriot/rpi-busybox-httpd", {80: 64441}, 0.005,  ram=100, ports=[80])
    # deployer.deploy_dockers(["148.88.227.232", "148.88.227.179"], "hypriot/rpi-busybox-httpd", {80: 64442}, 0.006, ram=500, ports=[80])
    # deployer.deploy_dockers(["148.88.227.232", "148.88.227.179"], "hypriot/rpi-busybox-httpd", {80: 64443}, 0.007, ram=50, ports=[80])
    # deployer.deploy_dockers(["148.88.227.232", "148.88.227.179"], "hypriot/rpi-busybox-httpd", {80: 64444}, 0.009, ram=10, ports=[80])


    #put this in thread?

    logging.info("RESTful service is running")

#Have a placeholder SDN input to get detailed location and context aware data? Should this not be done at the provisioner? It depends on what orchestrator it is attached to.
#Generate topology from devices available (update variables used for REST)
  #  while running:
