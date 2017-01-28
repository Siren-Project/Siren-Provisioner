#Main class.
from Discovery import *
from RestService import *
from Deployer import *
from LifecycleManager import *
import logging
import threading
import signal

import sys, os

from random import randint

#from time import sleep
class Provisioner:


    #Threaded function
    def start_rest(deployer, discovery, lifecycle):
        rest = RestService(deployer, discovery, lifecycle)
        #Handle thread kill here?

    def rand_provision(deployer):
        with open('nodes.json') as json_data:
            ips = json.load(json_data)['nodes']
            #FIXME Now invalid as nodes are loaded dynamically
        deployer.deploy_dockers(ips, "lyndon160/service_a", {80: randint(50000, 64444)}, randint(5, 9)*0.001,
                                ram=randint(10, 50), ports=[80])

    def signal_handler(signal, frame):
        print('Killed')
        os._exit(1)



    running = True
    logging.basicConfig(level=logging.INFO)
    discovery = Discovery()

    lifecycle_manager = LifecycleManager(discovery)
    deployer = Deployer(discovery, lifecycle_manager)


    threading.Thread(target=start_rest, args=(deployer, discovery, lifecycle_manager)).start()


    logging.info("RESTful service is running")


    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()






#Have a placeholder SDN input to get detailed location and context aware data? Should this not be done at the provisioner? It depends on what orchestrator it is attached to.
#Generate topology from devices available (update variables used for REST)
  #  while running:
