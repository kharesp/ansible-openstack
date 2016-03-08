#!/bin/bash

SUBNET_INTERFACE_EXISTS=$(neutron router-port-list $1 | grep $2)
if [ -z "$SUBNET_INTERFACE_EXISTS" ]; then
	neutron router-interface-add $1 $2
fi
