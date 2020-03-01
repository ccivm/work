from scapy.all import *
import base64
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
from threading import Timer
import time
import string
from _pydecimal import Decimal
from socket import *
import base64
from socket import *

print("初始化!!......")
 
def Get_connect(ip): #进行TCP连接，连接成功返回TCP套接字对象
    ADDR = (ip, 8080)          #目的端口
    tcpCliSock = socket(AF_INET, SOCK_STREAM)  # 创建tcp套接字
    tcpCliSock.connect(ADDR)
    print('连接成功！！！')
    return tcpCliSock

def Encode_base64(str): #传入字符串，返回base64加密后的bytes类型字符串
    encode_data = base64.b64encode(str.encode('utf-8'))

    return encode_data
def TCP_3(myip, myport):
	print('-----------wait---------')
	while True:
		s = sniff(filter="tcp and dst net "+myip+" and dst port "+str(myport), count=1) #监听向主机发来的数据包
		if s[0]["TCP"].flags == 'S':#当收到SYN请求时，发送SYN+ACK，等待回复的ACK
			#s[0].show()			
			ValueOfPort=s[0].sport
			SeqNr=s[0].seq
			AckNr=s[0].seq+1
			dstIP = s[0]["IP"].src
			print('dstIP:',dstIP)
			ip=IP(src=myip, dst=dstIP)
			TCP_SYNACK=TCP(sport=80, dport=ValueOfPort, flags="SA", seq=SeqNr, ack=AckNr,options=[('MSS',1440),('SAckOK','')])
			pkt_SA=ip/TCP_SYNACK
			#pkt_SA.show()
			ANSWER=sr1(pkt_SA, verbose=False)
			#ANSWER.show()
		

               
		if ANSWER["TCP"].flags == 'A' :  #当收到ACK回复，三次握手建立完成，开始监听数据包发送！！
			print('三次握手建立完成！！！')
			break
def TCP_DATA(myip, myport):
	data_list = [[],[]]
	#PA_count  = 0
	print('正在接收！！！')
	while True:
		#print('正在接收！！！')
		x = sniff(filter="tcp and dst net "+myip, count=1) #监听向主机发来的数据包			
		if x[0]["TCP"].flags == 'PA':      #收到结束标志！
			#PA_count=PA_count+1
			data_list[0].append(x[0]["TCP"].load.decode("utf-8","replace"))
			data_list[1].append(x[0]["TCP"].seq)
			dstIP = x[0]["IP"].src
			send(IP(dst=dstIP)/TCP(sport=x[0].dport,dport=x[0].sport,flags="A",seq=1,ack=x[0].seq+len(x[0]["TCP"].load)),verbose=False)
		if x[0]["TCP"].flags == 'FA':
			print('___________over___________')
			break
	return data_list
def scapy_rev(myip,myport):
	TCP_3(myip,myport)                 #进行握手
	data_list=TCP_DATA(myip, myport)   #接受数据并返回表
	whereis_seq=data_list[0].index('a2V5X2RhdGFfa2V5')+1  # 通过key包位置找到约定信息
	datas1=data_list[0][whereis_seq]
	datas=base64.b64decode(datas1)             #提取约定信息
	#print(data_list[1])
	hidden_seq=data_list[1][int(datas)-1]      #根据约定信息找到修改值
	#print('hidden is',int(datas))
	print('hidden seq is',hidden_seq)
	return hidden_seq
if __name__ == '__main__':
	myip   =   '192.168.1.109'#input('请你输入的IP地址: ')
	myport =     80#int(input('请你输入主机端口号: '))
	msg=scapy_rev(myip,myport)
	dst_ip = "127.0.0.1"#input('dst_server IP')
	tcpCliSock = Get_connect(dst_ip)
	data = str(msg)
	encode_data = Encode_base64(data)
	tcpCliSock.send(encode_data)
	print('发送完成')
	data_res = tcpCliSock.recv(1024)
	if not data_res:
		print('没有数据')
	print(data_res.decode('utf-8'))
	tcpCliSock.close()
