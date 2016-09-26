# Siren-Provisioner
A VNF provisioner for the Siren project. This is intended to be a modular component that could be used with higher level orchestration logic (such as **). At the moment, it exposes the infrastructure topology (location of available resouces and the time they are held up for) through a RESTful interface. For provisioning of resources, it accepts TOSCA, YAML and Docker files through a RESTful interface, to deploy the service, it uses the docker remote API. 


**Complementary component to this: https://github.com/broadbent/airship


For visualisation of the provsioner and the Fog infrastructure see: https://github.com/lyndon160/Siren-Visualiser


##  Northbound RESTful API

Example usage: GET http://127.0.0.1:60000/nodes

### GET

/nodes

/nodes/{id}

### POST

/provision_dockers

### DELETE
/remove_service_by_id

/remove_service
