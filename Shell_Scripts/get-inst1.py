from pprint import pprint
import boto
from boto import ec2

temphosts = '/home/ubuntu/midproject/hosts'
k8smaster_role_vars = '/home/ubuntu/midproject/roles/k8s_master/vars/main.yml'
k8sminion_role_vars = '/home/ubuntu/midproject/roles/k8s_minion/vars/main.yml'
tfvars = '/home/ubuntu/terraform.tfvars'
#consul_install_client = '/home/ubuntu/midproject/Consul_Scripts/consul_client_install_config.sh'

f=open(tfvars, 'r')
AWS_ACCESS_KEY_ID=(((f.readline()).replace('aws_access_key = "','')).replace('"','')).rstrip()
AWS_SECRET_ACCESS_KEY=(((f.readline()).replace('aws_secret_key = "','')).replace('"','')).rstrip()


def get_instances():
    instancelist = []
    ec2conn = ec2.connection.EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    reservations = ec2conn.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for i in instances:
        if("MidProject" in (str(i.tags[u'Name'])) and str(i.private_ip_address)!='None'):
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

    for i in instancelist:
      if(i[0]=='MidProjectAnsible'):
         ansibleoutputstring1 = str('[control1]')
         ansibleoutputstring2 = str('control1 ansible_host=') + i[1]

      if(i[0]=='MidProjectKubernetesMaster'):
         kubernetesmasteroutputstring1 = str('[kubernetesmaster]')
         kubernetesmasteroutputstring2 = str('kubernetesmaster ansible_host=') + i[1] 
         kubernetesmasterip = str(i[1])

      if(i[0]=='MidProjectKubernetesMinion1'):
         kubernetesminion1outputstring1 = str('[kubernetesminion1]')
         kubernetesminion1outputstring2 = str('kubernetesminion1 ansible_host=') + i[1]          
         kubernetesminion1ip = str(i[1])

      if(i[0]=='MidProjectKubernetesMinion2'):
         kubernetesminion2outputstring1 = str('[kubernetesminion2]')
         kubernetesminion2outputstring2 = str('kubernetesminion2 ansible_host=') + i[1]          
         kubernetesminion2ip = str(i[1])         

      if(i[0]=='MidProjectJenkinsMaster'):
         jenkinsmasteroutputstring1 = str('[jenkinsmaster]')
         jenkinsmasteroutputstring2 = str('jenkinsmaster ansible_host=') + i[1]         

    allvars1 = str('[all:vars]')
    allvars2 = str('ansible_user=ubuntu')
    allvars3 = str('ansible_ssh_private_key_file=/home/ubuntu/midproject/id_rsa')

    f = open(temphosts,'w')
    f.write(ansibleoutputstring1 + '\n' + ansibleoutputstring2 + '\n' + '\n' )
    f.write(kubernetesmasteroutputstring1 + '\n' + kubernetesmasteroutputstring2 + '\n' + '\n' )    
    f.write(kubernetesminion1outputstring1 + '\n' + kubernetesminion1outputstring2 + '\n' + '\n' )    
    f.write(kubernetesminion2outputstring1 + '\n' + kubernetesminion2outputstring2 + '\n' + '\n' )           
    f.write(jenkinsmasteroutputstring1 + '\n' + jenkinsmasteroutputstring2 + '\n' + '\n' )    
    f.write(allvars1 + '\n' + allvars2 + '\n' + allvars3 + '\n' + '\n' )
    f.close()

    f = open(k8smaster_role_vars,'a')
    f.write('k8s_master_ip: "' + kubernetesmasterip + '"\n' )
    f.close()
    f = open(k8sminion_role_vars,'a')
    f.write('k8s_master_ip: "' + kubernetesmasterip + '"\n' )
    f.close()
    
    #f = open(consul_install_client,'r')
    #filedata = f.read()
    #f.close()
    #newdata = filedata.replace("192.168.100.101",kubernetesminion1ip)
    #f = open(consul_install_client,'w')
    #f.write(newdata)
    #f.close()


if __name__ == "__main__":
    main()
