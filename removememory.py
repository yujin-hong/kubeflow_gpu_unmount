import requests
import json
import threading
import time
import paramiko
from paramiko import AutoAddPolicy

url = 'your-prometheus-address'

def check_gpu_usage(gpu_ip, gpu_name):
    usagePARAM = 'query=utilization_gpu'
    r = requests.get(url, params=usagePARAM)
    c = r.content.decode('utf-8')
    json_data = json.loads(c)
    results = json_data['data']['result']
    for result in results:
        if(result['metric']['gpu']==gpu_name and result['metric']['instance']==gpu_ip):
            return int(result['value'][1])
#     print(results)
#     for result in results:
        
def check_gpu_pid(gpu_ip, gpu_name):
    pidPARAM = 'query=gpu_using_pid'
    r = requests.get(url, params=pidPARAM)
    c = r.content.decode('utf-8')
    json_data = json.loads(c)
    results = json_data['data']['result']
    for result in results:
        if(result['metric']['gpu']==gpu_name and result['metric']['instance']==gpu_ip):
            return int(result['value'][1])
        
def check_gpu_memory(gpu_ip, gpu_name):
    pidPARAM = 'query=memory_used'
    r = requests.get(url, params=pidPARAM)
    c = r.content.decode('utf-8')
    json_data = json.loads(c)
    results = json_data['data']['result']
    for result in results:
        if(result['metric']['gpu']==gpu_name and result['metric']['instance']==gpu_ip):
            return int(result['value'][1])        
            
while True:
    PARAM = 'query=memory_used'
    r = requests.get(url, params=PARAM)
    c = r.content.decode('utf-8')
    json_data = json.loads(c)
    results = json_data['data']['result']

    gpu_ip_set=set([])
    gpu_name_set=set([])

    for result in results:
        gpu_ip = result['metric']['instance']    
        gpu_ip_set.add(gpu_ip)
        gpu_name = result['metric']['gpu']
        gpu_name_set.add(gpu_name)

    for result in results:
        gpu_ip = result['metric']['instance']
        gpu_name = result['metric']['gpu']
        gpu_memory = check_gpu_memory(gpu_ip, gpu_name)
#         print(gpu_ip, gpu_name, gpu_memory)

        if gpu_memory!=0 :
            gpu_usage = check_gpu_usage(gpu_ip, gpu_name)
            gpu_pid = check_gpu_pid(gpu_ip, gpu_name)
            if(int(gpu_usage)==0):
    #             print(gpu_usage, gpu_pid)
                termi=0
                for ip in gpu_ip_set:
                    for name in gpu_name_set:
                        tempid = check_gpu_pid(ip,name)
    #                     print(tempid)
    #                     print(gpu_pid)
                        if(tempid==gpu_pid):
                            timer=1
                            while timer<10:
    #                             print(timer)
                                if(check_gpu_usage(ip, name)!=0):
                                    termi=1
                                    break
                                timer=timer+1
                                time.sleep(1)
                            if termi==1:
                                break
                    if termi==1:
                        break
                if termi==0:
                    print(gpu_pid)
                    client = paramiko.SSHClient()
                    client.load_system_host_keys()
                    client.set_missing_host_key_policy(AutoAddPolicy())
                    node_host = gpu_ip.split(':')[0]
                    user_name = 'your-user-name'
                    user_password = 'your-user-password'
                    kill_command = 'kill -9 ' + str(gpu_pid)
                    client.connect(hostname=node_host, username=user_name, password=user_password)
                    stdin, stdout, stderr = client.exec_command(kill_command)
                    #stdin, stdout, stderr = client.exec_command('kill -9 36266')
                    # print (stdout.read())
                    client.close()
                    time.sleep(20)

        print('\n')
    time.sleep(60)
