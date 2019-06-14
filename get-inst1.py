from pprint import pprint
import boto
from boto import ec2

temphosts = '/home/ubuntu/midproject/hosts'
tfvars = '/home/ubuntu/terraform.tfvars'
f=open(tfvars, 'r')
AWS_ACCESS_KEY_ID=(((f.readline()).replace('aws_access_key = "','')).replace('"','')).rstrip()
AWS_SECRET_ACCESS_KEY=(((f.readline()).replace('aws_secret_key = "','')).replace('"','')).rstrip()


def get_instances():
    instancelist = []
    ec2conn = ec2.connection.EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    reservations = ec2conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for i in instances:
        if("MidProject" in (str(i.tags[u'Name']))):
            instance=[]
            servername=str(i.tags[u'Name'])
            privateip=str(i.private_ip_address)
            availabilityzone=str(i._placement)
            region=(str(i.region)).replace('RegionInfo:','')
            subnetid=str(i.subnet_id)
            vpcid=str(i.vpc_id)
            instance.append(servername)
            instance.append(privateip)
            instance.append(availabilityzone)
            instance.append(region)
            instance.append(subnetid)
            instance.append(vpcid)
            instancelist.append(instance)
    return instancelist


def main():
    instancelist = get_instances()
    listcount=len(instancelist)
    blankline = ""

    for i in instancelist:
      if(i[0]=='MidProjectAnsible'):
         ansibleoutputstring1 = str('[control1]')
         ansibleoutputstring2 = str('control1 ansible_host=') + i[1]

      if(i[0]=='MidProjectJenkins'):
         jenkinsoutputstring1 = str('[jenkins]')
         jenkinsoutputstring2 = str('jenkins ansible_host=') + i[1]         

      if(i[0]=='MidProjectSlave'):
         slaveoutputstring1 = str('[app]')
         slaveoutputstring2 = str('node-1 ansible_host=') + i[1]

    allvars1 = str('[all:vars]')
    allvars2 = str('ansible_user=ubuntu')
    allvars3 = str('ansible_ssh_private_key_file=/home/ubuntu/midproject/id_rsa')

    f = open(temphosts,'w')
    f.write(ansibleoutputstring1 + '\n' + ansibleoutputstring2 + '\n' + '\n' )
    f.write(jenkinsoutputstring1 + '\n' + jenkinsoutputstring2 + '\n' + '\n' )    
    f.write(slaveoutputstring1 + '\n' + slaveoutputstring2 + '\n' + '\n' )
    f.write(allvars1 + '\n' + allvars2 + '\n' + allvars3 + '\n' + '\n' )
    f.close()


if __name__ == "__main__":
    main()
