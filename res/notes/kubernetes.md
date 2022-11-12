### Pods = abstraction over a container (each gets their own IP)
### Node is a physical or virtual device that can run containers

### if a pod dies then its IP changes but this is where services come in...
### services have a permanent IP address where the lifecycle of the pod and server and not connected

### external service: exposes a port so you can access what you are running

### ingres allows you to set a good ip (as opposed to numbers) and makes it HTTPS instead of HTTP (makes it accessible)

### config map = external configuration of your application (such as URL's of database/services etc...)

# DONT PUT CREDENTIALS INTO A CONFIG MAP - use secret instead (stores in base64 as opposed to plaintext)

<hr>

### volumes: allow data to persist (you need something to store data like a harddrive)

### service is also a load balancer

### deployment = blueprint for pods (this specifies number of pods needed)

### DB cant be replicated via deployment because it has state

### stateful set = is like deployment but for things with state to prevent overwrites and shit (locks files etc...) - not as easy as deployments (thats why a lot of people will keep them seperate)

### must install kubelet, kube proxy and container software on all nodes

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

### Generally there will be multiple masters in a cluster of nodes - API server is load balanced and etcd acts as distributed storage across all master nodes

### master nodes are more improtant but generally have less resources as they do less

#### minikube allows master processes and worker processes to run on a single node together by using a virtual machine

#### kubectl is a command line interface