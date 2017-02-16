# Siren's Provisioner
A VNF provisioner for the Siren project. This is intended to be a modular component that could be used with higher level orchestration logic (such as **). At the moment, it exposes the infrastructure topology (location of available resouces and the time they are held up for) through a RESTful interface. For provisioning of resources, it accepts TOSCA YAML and Docker files through a RESTful interface, to deploy the service, it uses the docker remote API. 


**Complementary component to this: https://github.com/broadbent/airship


For visualisation of the provisioner and the Fog infrastructure see: https://github.com/lyndon160/Siren-Visualiser

## Installation and running

Siren's Provisioner is currently developed in python, it requires version 2.7 to be installed. 

Clone this repository:

```
git clone https://github.com/lyndon160/Siren-Provisioner.git
```

Pip requirements TODO:

```
pip install -r requirements.txt
```

To run the provsioner, simply do:

```
python ./Provisioner.py
```

## TODO
* Dynamic discovery; Allow new devices to join and leave the infrastructure.
* Service lifecycle with failover.
* Make threads safe.

##  Northbound RESTful API

Example usage: GET http://127.0.0.1:60000/nodes

All post requests take JSON input.

For a simple orchestration program, only /nodes and /provision_x should be required.



### GET
#### nodes
This returns information about all of the available nodes as list like this one: [{"reserved_memory": 200, "available_memory": 800, "total_memory": 1024, "id": "148.88.227.179", "arch": "armv7l", "location": "residence"}, {"reserved_memory": 0, "available_memory": 1024,  "total_memory": 1024, "id": "148.88.227.232", "arch": "armv7l", "location": "residence"}]

```
/nodes
```

#### nodes/{id}
This returns information about a single node. Not sure how useful this is.

```
/nodes/{id}
```


#### nodes/containers
This returns information similar to nodes but includes running containers
```
/nodes/containers
```



### POST
#### provision_dockers
This provisions a docker image to multiple devices for a set amount of time with a reservation on RAM

This requires:
[List nodes] [String image_name] [Int ram] [Int hours]

```
/nodes/provision_dockers
```

#### provision_toscas
TODO
```
/provision_toscas
``` 


### DELETE
#### remove_service_by_id
```
/remove_service_by_id
```

#### remove_service

```
/remove_service
```
