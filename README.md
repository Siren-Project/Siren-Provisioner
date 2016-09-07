# Siren-Provisioner
A VNF provisioner for the Siren project. This is intended to be a modular component that could be used with higher level orchestration logic (such as **). At the moment, it exposes the infrastructure topology (location of available resouces and the time they are held up for) through a RESTful interface. For provisioning of resources, it accepts TOSCA, YAML and Docker files through a RESTful interface, to deploy the service, it uses the docker remote API. 


**Complementary component to this: https://github.com/broadbent/airship
