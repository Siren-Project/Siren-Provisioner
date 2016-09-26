import logging
from threading import Thread
import time
from time import sleep

class LifecycleManager:


    services = []


        #duration is in hours, supports doubles
    def register_service(self, node_ids, duration):
        self.append({node_ids, time.time()+(duration*60*60)})
        #add duration to current time
        pass

    def monitor_and_enforce(self):
        while True:
            logging.info("Hi %d", int(time.time()))
            for service in services:
                service
            sleep(1)


    def __init__(self, discovery):
        self.discovery = discovery
        thread = Thread(name="monitor_and_enforce", target=self.monitor_and_enforce)
        thread.start()