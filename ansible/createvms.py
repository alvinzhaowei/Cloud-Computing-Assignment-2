import subprocess
import json
import time
import os
import sys

vmnum = 4

print('Creating virtual machines on Nectar.')
i=0
while (i < vmnum):
    # vm name 
    name = 'node' + str(i + 1)
    # private key for connection
    subprocess.call('openstack keypair create key cloud > key cloud.key',
	shell=True, stdout=subprocess.PIPE)
    subprocess.call('sudo chmod 600 key'+name+'.pem',shell=True,
	 stdout=subprocess.PIPE)
    # create new vm add the security group ssh
    subprocess.call('openstack server create '+name+
    ' --image c8663e68-921c-4e0'+\
	'a-9048-d9e042a4b41f --flavor 1 --key-name "key'+name+\
	'" --security-group ssh ',
    shell=True, stdout=subprocess.PIPE)
    i = i+1


#check if vms are built

while (True):
    check = json.loads(subprocess.check_output('openstack server list -f json',	shell=True).decode("utf-8"))
    count = 0
    for result in check:
        if result['Status']=='BUILD':
            count = count + 1
    if count == 4:
        break
        

print("Virtual machines are built.")

# Builds a list of vms
VMs = json.loads(subprocess.check_output('openstack server list -f json',
	shell=True).decode("utf-8"))

# Stores the information of VMs to make ansible file.
VMinfor = []
for i in VMs:
    VMinfor.append(json.loads(subprocess.check_output('openstack server show '+\
	i['Name']+' -f json',shell=True).decode("utf-8")))


with open("hosts",'w+') as new_file:
    new_flie.write("[vms]")
    host_ip=""
    host_key=""
    for i in VMinfor:
        new_flie.write('\n')
        host_ip=i['accessIPv4']
        new_flie.write(host_ip)
        new_flie.write(' ansible_ssh_private_key_file=')
        host_key=i['key_name']
        new_flie.write(host_key)
        new_flie.write('.key')
    new_flie.write('\n')
    new_flie.write('\n')
    new_flie.write("[webserver]")
    new_flie.write('\n')
    new_flie.write(host_ip)
    new_flie.write(' ansible_ssh_private_key_file=')
    new_flie.write(host_key)
    new_flie.write('.key')
    new_flie.write('\n')
    new_flie.write('\n')
    new_flie.write("[couchdb]")
    new_flie.write('\n')
    new_flie.write(host_ip)
    new_flie.write(' ansible_ssh_private_key_file=')
    new_flie.write(host_key)
    new_flie.write('.key')
    new_flie.close()
