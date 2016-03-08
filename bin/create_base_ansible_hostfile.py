import argparse

parser = argparse.ArgumentParser(description= 'This script creates the ansible host file called openstack_instances, which describes the base openstack deployment of VMs. The script takes three arguments which designate the number of private networks to create, the cidr pattern to use for these private network\'s subnet and the number of VMs to launch per private network')

parser.add_argument("nw",type=int,help="specifies the number of private networks to create")
parser.add_argument("vm",type=int,help="specifies the number of VMs to create per private network")
parser.add_argument("cidr",help="specifies the cidr pattern to use while creating subnets for the private networks. For example: 10.2.x.0/24. If numNw passed is 5; 10.2.1.0/24, 10.2.2.0/24,10.2.3.0/24,10.2.4.0/24 and 10.2.5.0/24 are the subnets that will be created for the 5 private networks in openstack")

args=parser.parse_args()
print ("Creating base ansible host file 'inventory/openstack_instances' with {0} private networks and {1} VMs per private network. CIDR pattern:{2}".format(args.nw,args.vm,args.cidr))

f= open('inventory/openstack_instances','w')
for x in range(0,args.nw):
	network_id=x+1
	vm_lower_bound= (args.vm * x)+1
	vm_upper_bound=  vm_lower_bound + (args.vm-1)
	cidr=args.cidr.replace('x',str(network_id))

	#Write network group
	f.write("[nw{0}]\n".format(network_id))
	#Write host VMs belonging to this network group
	f.write("vm[{0}:{1}] nw=nw{2} subnet=subnet{3} cidr={4}\n\n"
		.format(vm_lower_bound,vm_upper_bound,network_id,network_id,cidr))

f.write("[openstack_instances:children]\n"); 
for x in range(0,args.nw):
	f.write("nw{0}\n".format(x+1))
	

f.close()
