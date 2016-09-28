# Siren-Provisioner
A VNF provisioner for the Siren project. This is intended to be a modular component that could be used with higher level orchestration logic (such as **). At the moment, it exposes the infrastructure topology (location of available resouces and the time they are held up for) through a RESTful interface. For provisioning of resources, it accepts TOSCA YAML and Docker files through a RESTful interface, to deploy the service, it uses the docker remote API. 


**Complementary component to this: https://github.com/broadbent/airship


For visualisation of the provsioner and the Fog infrastructure see: https://github.com/lyndon160/Siren-Visualiser


##  Northbound RESTful API

Example usage: GET http://127.0.0.1:60000/nodes

All post requests take JSON input.

For a simple orchestration program, only /nodes and /provision_x should be required.

### GET
'''bash
/nodes
'''
This returns a list such as [{"reserved_memory": 0, "total_memory": 1020391424, "id": "148.88.227.179", "arch": "armv7l", "location": "residence"}, {"reserved_memory": 0, "total_memory": 1020391424, "id": "148.88.227.232", "arch": "armv7l", "location": "residence"}]
'''bash
/nodes/{id}
'''
### POST
'''bash
'/provision_dockers
'''
[List nodes] This takes a list of IDs which correspond computes. (Get this information from /nodes) [String image_name] A single image name to be deployed accross the nodes. [Int ram] An ammount of RAM. [Int hours] A number of hours for the service to run.
'''bash
/provision_toscas' TODO
'''
### DELETE
'''bash
/remove_service_by_id
'''
'''bash
/remove_service
'''