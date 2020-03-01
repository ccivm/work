from scapy.all import *
import base64
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
from threading import Timer
import time
import xlrd
import string
from socket import *
import psutil
import base64
key1       =   'key_data_key'
key2       =   'yek_atad_yet'
key1s      =   base64.b64encode(key1.encode('utf-8'))
key2s      =   base64.b64encode(key2.encode('utf-8'))    #key值用于第3端寻找 约定信息  
def start_tcp(target_ip,target_port,source_port):
    print('正在握手')
    global sport,s_seq,d_seq                                                     #主要是用于TCP3此握手建立连接后继续发送数据
    try:
        #第一次握手，发送SYN包
        #ans     = sr1(IP(dst=target_ip)/TCP(dport=target_port,sport=source_port,seq=RandInt(),flags='S'),verbose=False)
        ans     = sr1(IP(dst=target_ip)/TCP(dport=target_port,sport=source_port,seq=0,flags='S',options=[('MSS',48),('SAckOK', '')]),verbose=False)
        #ans.show()
        sport   = ans[TCP].dport                                                 #源随机端口
        s_seq   = ans[TCP].ack                                                   #源序列号（其实初始值已经被服务端加1）
        d_seq   = ans[TCP].seq + 1                                               #确认号，需要把服务端的序列号加1
        #第三次握手，发送ACK确认包
        send(IP(dst=target_ip)/TCP(dport=target_port,sport=source_port,ack=d_seq,seq=s_seq,flags='A'),verbose=False)
        print('TCP三次握手成功！！')

    except Exception:
        print("TCP连接出错！！")
    return ans,d_seq,s_seq
def Read_excel(file_path):
    wb = xlrd.open_workbook(filename=file_path)#打开文件
    sheet1 = wb.sheet_by_index(0)#通过索引获取表格
    cols2 = sheet1.col_values(2)   #获取表单第3列的数据(间隔时间)
    cols3 = sheet1.col_values(3)   #获取表单第4列的数据（发包数量）
    cols4 = sheet1.col_values(4)   #获取表单第5列的数据（发包总字节数）
    return  cols2, cols3, cols4
    
def Read_txt(file_path):   #读txt文本
    info1 = []
    info2 = []
    for line in open(file_path):
        info1.append(line.split(',')[0])
        info2.append(line.split(',')[1])
    return info1, info2
def key_data_key(target_ip,target_port,my_ip):     #一条网络流量头部的3个包用K——D——K的方式标识了seq改变了的位置 以下皆称为约定信息
    ans,s_seq,d_seq=start_tcp(target_ip,target_port,source_port)
    ip = IP(src=my_ip,dst=target_ip)
    tcp = TCP(sport=ans[0].dport,dport=ans[0].sport,flags='PA',seq=s_seq,ack=d_seq,)
    pkt1 =ip/tcp/key1s       #key1包用于第3端检测约定
    time.sleep(1)
    send(pkt1,verbose=0) 
    print("_________1_________")
    ip = IP(src=my_ip,dst=target_ip)
    tcp = TCP(sport=pkt1.sport,dport=pkt1.dport,flags='PA',seq=17,ack=1)
    pkt2 =ip/tcp/datas1           #约定信息 存在位置
    time.sleep(1)
    send(pkt2,verbose=0)
    print("_________2_________")
    ip = IP(src=my_ip,dst=target_ip)
    tcp = TCP(sport=pkt2.sport,dport=pkt2.dport,flags='PA',seq=29,ack=1)
    pkt3 =ip/tcp/key2s
    time.sleep(1)
    send(pkt3,verbose=0)
    print('_________3_________')
def add_pkt(seq_value,blen,target_ip,target_port,my_ip):      #构造一个包并发包
    blenadd=int(blen)-40
    if blenadd <=0:
        blenadd=0
    if blenadd >= 1400:
        blenadd=1400
    seq_value=int(seq_value)
    datas4      =   ''.join(random.sample(string.ascii_letters*300 + string.digits, int(blenadd)))    #补充负载的字符集
    datas4      =   datas4.encode('utf-8')
    ip  = IP(src=my_ip,dst=target_ip)
    tcp = TCP(sport=source_port,dport=80,flags='PA',seq=seq_value,ack=1)  #附带seq隐蔽信息的包
    pkt =ip/tcp/datas4
    send(pkt,verbose=0)
def add_pkt_loop(info,seq_hidden,target_ip,target_port,my_ip):
	for i in range(3,len(info2)):
		blen=int(info2[i])-int(info2[i-1])
		if i==int(data1):   #如果是约定位数 就写入用户传递的seq_hidden
			add_pkt(seq_hidden,blen,target_ip,target_port,my_ip)
		else:                #如果不是约定位数 就写入txt根据计算得来的seq
			add_pkt(info2[i],blen,target_ip,target_port,my_ip)
		time.sleep(0.5)
def TCP_wave():
    print('FIN正在发送')
    send(IP(dst=target_ip)/TCP(dport=target_port,sport=source_port,flags=17),verbose=False) 
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

def seq_scapy(ip):
    ip = ip#"192.168.1.100"#Get_ip()
    dst_socket = Listen_con(ip)
    rev_msg = dst_socket.recv(1024)
    rev_msg_str =base64.b64decode(rev_msg.decode('utf-8'))
    rev_msg_int =int(base64.b64decode(rev_msg.decode('utf-8')))
    #print(rev_msg_int)
    send_msg = rev_msg
    dst_socket.send(send_msg)                    #读第一端发来的第一个数据

    #dst_socket = Listen_con(ip)
    rev_msg2 = dst_socket.recv(1024)
    rev_msg2_str =base64.b64decode(rev_msg2.decode('utf-8'))
    rev_msg2_int =int(base64.b64decode(rev_msg2.decode('utf-8')))
    #print(rev_msg2_int)
    send_msg2 = rev_msg2
    dst_socket.send(send_msg2)                   #读第一端发来的第二个数据
    return rev_msg_int,rev_msg2_int
if __name__ == '__main__':
    my_ip    ='192.168.1.104'
    rev_msg_int,rev_msg2_int=seq_scapy(my_ip)
    data1=str(rev_msg_int)
    datas1=base64.b64encode(data1.encode('utf-8'))
    target_ip   =   '192.168.1.109'#input('请你输入目的主机的IP地址: ')
    target_port =     80#int(input('请你输入目的主机端口号: '))
    source_port =   random.randint(1024, 65535)#源端口
    info1, info2,info3 = Read_txt('110.txt')
    print('读取完成')
    print('准备连接并发包')
    seq_hidden =rev_msg2_int#int(input('存储隐蔽信道内容（int）：'))
    time.sleep(0.5)
    key_data_key(target_ip,target_port,my_ip)
    add_pkt_loop(info2,seq_hidden,target_ip,target_port,my_ip)
    TCP_wave()
