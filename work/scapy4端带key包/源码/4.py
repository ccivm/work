from socket import *
import psutil
import base64
def Listen_con(ip):
    ADDR = (ip, 8080)
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)
    print('waitting for connect')
    tcpCliSock, addr = tcpSerSock.accept()
    print('连接成功！！！')
    return tcpCliSock

def Get_ip():
    info = psutil.net_if_addrs()  # 返回类似ipconfig的功能
    print(info['WLAN'][1][1])
    return info['WLAN'][1][1]

def seq_scapy():
    ip = "192.168.1.100"#Get_ip()
    dst_socket = Listen_con(ip)
    rev_msg = dst_socket.recv(1024)
    rev_msg_str =base64.b64decode(rev_msg.decode('utf-8'))
    rev_msg_int =int(base64.b64decode(rev_msg.decode('utf-8')))
    #print(rev_msg_int)
    send_msg = rev_msg
    dst_socket.send(send_msg)
    #dst_socket = Listen_con(ip)  
    return rev_msg_int
if __name__ == '__main__':
    rev_msg_int=seq_scapy()      #接收从scapy处理的seq信息  通过socket
    print(rev_msg_int)