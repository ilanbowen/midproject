from pprint import pprint
import boto
from boto import ec2

etc_hosts = '/etc/hosts'
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

    for i in instancelist:
      if(i[0]=='MidProjectJenkinsMaster' and i[1]!='None'):
         jenkinsmasterip = str(i[1])
         outputline = jenkinsmasterip + ' jenkinsmaster_server'
         f = open(etc_hosts,'a+')
         f.write(outputline)
         f.close()
         break


if __name__ == "__main__":
    main()
