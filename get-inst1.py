from pprint import pprint
import boto
from boto import ec2

temphosts = '/home/ubuntu/midproject/temphosts'
tfvars = 'terraform.tfvars'
f=open(tfvars, 'r')
AWS_ACCESS_KEY_ID=(((f.readline()).replace('aws_access_key = "','')).replace('"','')).rstrip()
AWS_SECRET_ACCESS_KEY=(((f.readline()).replace('aws_secret_key = "','')).replace('"','')).rstrip()


def get_instances():
    instancelist = []
    ec2conn = ec2.connection.EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    reservations = ec2conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for i in instances:
        if("MidProjectMaster" in (str(i.tags[u'Name'])) or "MidProjectSlave" in (str(i.tags[u'Name']))):
#        if(i.vpc_id=='vpc-092a67ba407262eef' and (i.private_ip_address=='192.168.100.100' or i.private_ip_address=='192.168.100.101')):

            instance=[]
            servername=str(i.tags[u'Name'])
            privateip=str(i.private_ip_address)
            availabilityzone=str(i._placement)
            region=(str(i.region)).replace('RegionInfo:','')
            subnetid=str(i.subnet_id)
            vpcid=str(i.vpc_id)

#            print("")
#            print(servername)
#            print(privateip)
#            print(availabilityzone)
#            print(region)
#            print(subnetid)
#            print(vpcid)

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
      if(i[0]=='MidProjectMaster'):
         masteroutputstring1 = str('[control1]')
         masteroutputstring2 = str('control1 ansible_host=') + i[1]

      if(i[0]=='MidProjectSlave'):
         slaveoutputstring1 = str('[app]')
         slaveoutputstring2 = str('node-1 ansible_host=') + i[1]

    allvars1 = str('[all:vars]')
    allvars2 = str('ansible_user=ubuntu')
    allvars3 = str('ansible_ssh_private_key_file=/home/ubuntu/midproject/id_rsa')
#    print(masteroutputstring1)
#    print(masteroutputstring2)
#    print(blankline)
#    print(slaveoutputstring1)
#    print(slaveoutputstring2)
#    print(blankline)
#    print(allvars1)
#    print(allvars2)
#    print(allvars3)

    f = open(temphosts,'w')
    f.write(masteroutputstring1 + '\n' + masteroutputstring2 + '\n' + '\n' )
    f.write(slaveoutputstring1 + '\n' + slaveoutputstring2 + '\n' + '\n' )
    f.write(allvars1 + '\n' + allvars2 + '\n' + allvars3 + '\n' + '\n' )
    f.close()


if __name__ == "__main__":
    main()
