# Systematic terms:
- *Pods*    = abstraction over a container (each gets their own IP)
- *Node*    = physical or virtual device that can run pods
- *Cluster* = manages a whole bunch of nodes

<br>

### must install kubelet, kube proxy and container software on all nodes
### minikube allows master processes and worker processes to run on a single node together by using a virtual machine
### kubectl is a command line interface

<br>

## Different kinds:
1. Deployment
2. Service
3. Statefulset
4.
5.

<br>
<br>
<hr>

## Master node does all the cool processing stuff
- add new nodes
- revive dead nodes
- is a cluster gateway
- acts as a gatekeeper for authentication as well 
    - has API server
    - scheduler (is smart and figures out what node will take care of a new job)
    - controller manager (detects when nodes die and tries to recover)
    - etcd - key value store for a clusters state

### even though master nodes are more improtant they generally have less resources (since they do less processing))

<br>

## Configurations:
- ConfigFile is like a .env **BUT everything is stored in plaintext so dont store credentials there**
    - external configuration of your application (such as URL's of database/services etc...)
- Secret is like a .env **BUT everything is stored in base64**
    - for passwords

<br>

## Making an IP visible
#### to make a service external set its type inside selector as LoadBalancer (exposes nodePort below)
#### nodePort is the port you need to access from the internet ranges from 30000 to 32767  

<br>

### **if a pod dies then its IP changes but this is where services come in...**

## This is where services come into play:
- they have a permanent IP address where the lifecycle of the pod and server and not connected
- ingres allows you to set a good ip (as opposed to numbers) and makes it HTTPS instead of HTTP

<br>

## Volumes:
### volumes: allow data to persist (you need something to store data like a harddrive)

<br>

### service, statefulset and deployments act as load balancers
### deployment = blueprint for pods (this specifies number of pods needed)
### DB cant be replicated via deployment because it has state
### stateful set = is like deployment but for things with state to prevent overwrites and shit (locks files etc...) - not as easy as deployments (thats why a lot of people will keep them seperate)

<br>
<br>
<hr>

# General information about YAML
## YAML has metadata, spec, status
### put template represents a container (which is in spec)

### labels and selectors are how you manage and enable connections to the containers
- labels are used to connect deployments and pods together (set them to the same thing)

## selectors allow services to connect to labels i.e service selector app: nginx and then metadata labels app:nginx connects the two

## pods need ports! 
1. In services: (internal maps to external)
    - protocol
    - port
    - targetport
2. Pods:
    ports: - containerPort (internal)

### order of creation matters create secret files before deployment

--- = creates a seperation in a yaml file  
generally deployment and services go in the same file thanks to this  

- to connect to database need:  
1. mongodb_server = address or internal service  

- which credentials to authenticate  
1. adminusername  
2. adminpassword  

#### clusterID = default

<br>

# Different YAML examples