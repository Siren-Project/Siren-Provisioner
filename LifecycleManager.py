import logging
# from threading import Thread
# from time import sleep
import time
import threading


class LifecycleManager:

    #Service id: ([List of nodes], duration secs)


        #duration is in hours, supports doubles
    def register_service(self, node_ids, duration, service_id):
        self.services[service_id] = (node_ids, time.time()+(duration*60*60))
        logging.info("Service time = %d seconds", duration*60*60)

    def monitor_and_enforce(self):
        services_to_pop = []
        logging.info("Running services %s", self.services.keys())
        #logging.info("%d", time.time())
        for service_id in self.services.keys():

            #logging.info("Service time left %d seconds", self.services[service_id][1]-time.time())
            if self.services[service_id][1]-time.time() < 1:
                services_to_pop.append(service_id)
                logging.info("Services to pop %s", services_to_pop)

        for service_id in services_to_pop:
            logging.info("Terminating service with service_id %d", service_id)
#            t = threading.Thread(target=self.terminate_service, args=service_id).start()
            self.terminate_service(service_id)
            self.services.pop(service_id)
        threading.Timer(10, self.monitor_and_enforce).start()

    def terminate_service(self, service_id):
        # get nodes associated with service
        for node_id in self.services[service_id][0]:
            threading.Thread(target=self.discovery.get_node(node_id).terminate_service,
                             args=(service_id,)).start()
            #self.discovery.get_node(node_id).terminate_service(service_id)


    def __init__(self, discovery):
        self.discovery = discovery
        self.services = {} #1: (["148.88.227.232"], time.time()+10), 2: (["148.88.227.179"], time.time()+5)
        thread = threading.Thread(target=self.monitor_and_enforce)
        thread.daemon = True
        thread.start()
