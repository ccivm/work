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
		x = sniff(filter="tcp and dst net "+myip, count=1) #监听向主机发来的数据包			
		if x[0]["TCP"].flags == 'PA':
			#print("_________________PA______________")      
			data_list[1].append(len(x[0]["TCP"].load))
			data_list[0].append(x[0]["TCP"].seq)
			dstIP = x[0]["IP"].src
			send(IP(dst=dstIP)/TCP(sport=x[0].dport,dport=x[0].sport,flags="A",seq=1,ack=x[0].seq+len(x[0]["TCP"].load)),verbose=False)
		if x[0]["TCP"].flags == 'FA':
			print('___________over___________')
			break
	return data_list
def scapy_rev(myip,myport):
	TCP_3(myip,myport)
	data_list=TCP_DATA(myip, myport)
	listlen=len(data_list[0])
	#print(listlen)
	m=0
	compared_list_xin=[]
		
	for i in range(1,listlen):
		#print(data_list[0][i-1],data_list[1][i-1])
		m=m+int(data_list[1][i-1])
		compared_list_xin.append(m)
	return compared_list_xin,data_list
def Read_txt(file_path):
    info1 = []
    info2 = []
    info3 = []
    for line in open(file_path):
        info1.append(line.split(',')[0])
        info2.append(line.split(',')[1])
        info3.append(line.split(',')[2])
    return info1,info2,info3	

def compared(compared_list_xin,compared_list_jiu):
    q=0
    w=0
    e=0
    r=0
    #print(len(compared_list_xin))
    for i in range (1,len(compared_list_xin)):
        m=compared_list_xin[i-1]-compared_list_jiu[i-1]	
        if m==1:
            q=q+1
        if m==2:
            w=w+1
        if m==3:
            e=e+1

    print("q is",q,"w is",w,"e is",e,"r is",r)
    if q>20:
        return 20
    #if w>40:
     #   return 30
   # if e>40:
      #  return 40
if __name__ == '__main__':
	myip   =   '192.168.1.109'#input('请你输入的IP地址: ')
	myport =     80#int(input('请你输入主机端口号: '))
	info1, info2,info3 = Read_txt('1.txt')
	compared_list_jiu=[]
	for i in range(1,len(info2)):
		if i==1:
			compared_list_jiu.append(int(info2[i-1]))
		else:	
			compared_list_jiu.append(int(info2[i-1]))
		
	compared_list_xin,data_list=scapy_rev(myip,myport)

	where_is=compared(compared_list_xin,compared_list_jiu)
	if where_is==20:
		print("method: +1,coordinate:20 ")
	print("seq_value is",int(data_list[0][where_is-1]))
	
	msg=int(data_list[0][where_is-1])
	dst_ip = "127.0.0.1"#input('dst_server IP')
	tcpCliSock = Get_connect(dst_ip)
	data = str(msg)
	encode_data = Encode_base64(data)
	tcpCliSock.send(encode_data)
	print('发送完成')
	data_res = tcpCliSock.recv(1024)
	if not data_res:
		print('没有数据')
    #print(data_res.decode('utf-8'))
	tcpCliSock.close()
