import pymysql
import sys
import random
from pythonping import ping
from sshtunnel import SSHTunnelForwarder


def send_command(data_ip, manager_ip, command):
    '''
    Execute the command on the specified slave IP with a SSHTunnel through the master's IP

            Parameters:
                    data_ip (str): data node IP
                    manager_ip (str): manager IP
                    command (str): SQL command
    '''
    with SSHTunnelForwarder(data_ip, ssh_username='ubuntu', ssh_pkey='myEc2-keypair.pem', remote_bind_address=(manager_ip, 3306)) as tunnel:
        conn = pymysql.connect(host=manager_ip, user='myUser',
                               password='myPassword', db='sakila', port=3306, autocommit=True)
        cursor = conn.cursor()
        cursor.execute(command)
        print(cursor.fetchall())
        return conn


def cstm_imp(nodes, mgmt_node_ip, command):
    '''
    Sends a command to the data node with the lowest response time.

            Parameters:
                    nodes (list): Data nodes IPs
                    mgmt_node_ip (str): Master Node IP
                    command (str): SQL command
    '''
    min = 100000000
    best_slave = nodes[0]
    for slave in nodes:
        ping_time = ping(target=slave, count=1, timeout=2).rtt_avg_ms
        if ping_time < min:
            best_slave = slave
            min = ping_time
    print('Sending Request to : ', best_slave)
    send_command(best_slave, mgmt_node_ip, command)


if __name__ == "__main__":
    management_node_ip, node1_ip, node2_ip, node3_ip, imp, command = sys.argv[
        1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
    if imp == "direct":
        send_command(management_node_ip, management_node_ip, command)
    elif imp == "random":
        data_node_ip = random.choice([node1_ip, node2_ip, node3_ip])
        print('Sending Request to : ', data_node_ip)
        send_command(data_node_ip, management_node_ip, command)
    elif imp == "customized":
        cstm_imp([node1_ip, node2_ip,
                  node3_ip], management_node_ip, command)
