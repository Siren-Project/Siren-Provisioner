# Siren-Provisioner
A VNF provisioner for the Siren project. This is intended to be a modular component that could be used with other higher layer orchestration logic. At the moment, it exposes the infrastructure topology (location of available resouces and the time they are held up for) through a RESTful interface. For provisioning of resourcves, it accepts TOSCA, YAML and Docker files, again through a RESTful interface, to describe a service and uses the docker API to put them on to the infrastructure. 


Complementary component to this: https://github.com/broadbent/airship
