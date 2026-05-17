[all]
localhost ansible_connection=local

[managers]
manager1 ansible_host=localhost ansible_connection=local

[workers]
%{ for i in range(vm_count) ~}
worker${i+1} ansible_host=192.168.1.${10+i} ansible_user=ubuntu
%{ endfor ~}

[all:vars]
app_name=${app_name}
environment=${environment}
