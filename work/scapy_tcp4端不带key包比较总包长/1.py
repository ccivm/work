from socket import *
import base64
from socket import *


def Get_connect(ip): #进行TCP连接，连接成功返回TCP套接字对象
    ADDR = (ip, 8080)          #目的端口
    tcpCliSock = socket(AF_INET, SOCK_STREAM)  # 创建tcp套接字
    tcpCliSock.connect(ADDR)
    print('套接字建立连接')
    return tcpCliSock

def Encode_base64(str): #传入字符串，返回base64加密后的bytes类型字符串
    encode_data = base64.b64encode(str.encode('utf-8'))

    return encode_data
if __name__ == '__main__':
    dst_ip = "192.168.1.104"#input('dst_server IP')
    tcpCliSock = Get_connect(dst_ip)
           # 输入俩个数据
    data = input('请任意输入数字检测通道是否成功')
    encode_data = Encode_base64(data)

    tcpCliSock.send(encode_data)
    print('通道成功，可以发送信息')
    data_res = tcpCliSock.recv(1024)
    if not data_res:
        print('没有成功')
    #print(data_res.decode('utf-8'))
    data = input('请输入携带的信息（数字）')
    encode_data = Encode_base64(data)

    tcpCliSock.send(encode_data)
    print('发送完成')
    data_res = tcpCliSock.recv(1024)
    if not data_res:
        print('没有数据')
    print("远代已经接受",data_res.decode('utf-8'))
    tcpCliSock.close()
