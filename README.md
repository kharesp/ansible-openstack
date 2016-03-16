# ansible-openstack
#####Ansible for provisioning openstack and configuring a mesos cluster

The ansible scripts in this repository help in:

1. Provisioning a cluster of VMs in openstack
2. Configuring the VMs on the basis of assinged roles

The provisioning script will create a configurable number of private networks in Opensack,
connect each of these private networks to an external-network and provision a configurable 
number of VMs within each private network. 

An example deployment with 6 private networks (nw1 to nw6),
each connected to an external network (ext-nw) and having 1 VM each,is shown in the following image: 
![alt text](https://github.com/kharesp/ansible-openstack/blob/master/deployment.png "Provisioned Openstack deployment")

The host files specifiying the deployment and roles are present under `./inventory` directory. 

1. `./inventory/openstack_instances` host file specifies the desired openstack deployment (i.e. the number of private networks and VMs in each private network)
 
2. `./inventory/roles` file specifies the roles assigned to the provisioned VMs. 

Example `./inventory/openstack_instances` file: 
```
[nw1]
vm[1:1] nw=nw1 subnet=subnet1 cidr=10.2.1.0/24

[nw2]
vm[2:2] nw=nw2 subnet=subnet2 cidr=10.2.2.0/24

[nw3]
vm[3:3] nw=nw3 subnet=subnet3 cidr=10.2.3.0/24

[nw4]
vm[4:4] nw=nw4 subnet=subnet4 cidr=10.2.4.0/24

[nw5]
vm[5:5] nw=nw5 subnet=subnet5 cidr=10.2.5.0/24

[nw6]
vm[6:6] nw=nw6 subnet=subnet6 cidr=10.2.6.0/24

[openstack_instances:children]
nw1
nw2
nw3
nw4
nw5
```
The `./inventory/openstack_instances` host file can be created using `./bin/create_base_ansible_hostfile.py` script by 
specifying the number of private networks, VMs per private network and cidr pattern for the private networks: 

`python bin/create_base_ansible_hostfile.py 6 1 10.2.x.0/24`


```
python bin/create_base_ansible_hostfile.py -h
usage: create_base_ansible_hostfile.py [-h] nw vm cidr

This script creates the ansible host file called openstack_instances, which
describes the base openstack deployment of VMs. The script takes three
arguments which designate the number of private networks to create, the cidr
pattern to use for these private network's subnet and the number of VMs to
launch per private network

positional arguments:
  nw          specifies the number of private networks to create
  vm          specifies the number of VMs to create per private network
  cidr        specifies the cidr pattern to use while creating subnets for the
              private networks. For example: 10.2.x.0/24. If nw passed is
              5; 10.2.1.0/24, 10.2.2.0/24,10.2.3.0/24,10.2.4.0/24 and
              10.2.5.0/24 are the subnets that will be created for the 5
              private networks in openstack
```

Custom roles for the provisioned VMs can be specified in the `./inventory/roles` file. For example, to create a mesos cluster
with vm1 as mesos-master and remaining vm2-vm6 as mesos-slaves, the `./inventory/roles` file would look like this: 
```
[mesos_masters]
vm1

[mesos_slaves]
vm[2:6]
```

#####To execute the ansible scripts for Openstack deployment and provisioning, perform the following steps:

1. As we might not have sufficient number of public/floating ips available, ansible scripts in this repository do not 
associate a floating/public ip to the provisioned VMs. (Except for mesos-master VM, which is assigned a public-ip for easy
access to marathon and mesos-master gui, although it is not mandatory). Hence, we need to have a pubicly accessible VM in
openstack which can act as a gateway to access the provisioned VMs with private IPs. 

    In order to access the provisioned VMs with private IPs via a publicly accessible VM in openstack,
    perform the following steps:

    1.1 Create a VM in openstack and associte a floating IP to it. 
    
    1.2 Configure the openstack gateway information in $HOME/.ssh/config or 
       /etc/ssh/ssh_config on the workstation from which you will be running the ansible scripts, as follows:
       ```
       Host openstack-gw
       Hostname <public-ip-of-openstack-gw>
       User <username-for-accessing-openstack-gw>
       IdentityFile <path-to-ssh-key-for-accessing-openstack-gw>
       
       Host 10.2.*.*
       User <username-for-accessing-provisioned-VMs-with-private-ips>
       IdentityFile <path-to-ssh-key-for-accessing-provisioned-VMs-with-private-ips>
       ProxyCommand ssh openstack-gw nc %h 22
       ```

2. Source your openstack.rc file in the terminal from which you wish to execute the ansible scripts. This will make 
the required openstack authorization information like `OS_AUTH_URL`,`OS_TENANT_ID`,`OS_TENANT_NAME`,`OS_USERNAME`, `OS_REGION_NAME`
available to ansible as environment variables. 

3. Configure the type of VM image to provision, ssh key-pair name for openstack VMs, VM flavor, security group and 
external router information in `./roles/openstack_instances/vars/main.yml`: 
    ```
    ---
    image: ubuntu-14.04
    key_name: example_access_keypair
   flavor: ps.small
   security_groups: default
   ext_router_name: example_ext_router
   ```
4. Execute cluster.yml playbook with:

   `ansible-playbook -vvv cluster.yml` 

   This will provision the VMs in openstack and as per the roles specified in `./inventory/roles` file, configure a mesos cluster. 



#####Brief description of ansible scripts 




