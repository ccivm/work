# -*- coding: UTF-8 -*-
import dpkt
import scapy
from scapy.all import *
from scapy.utils import PcapReader
import xlwt
import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt
def excel_line_to_list():
    df = pd.read_excel("pcap_analist.xls", usecols=[1, 6],names=None)  # 读取两列，并不要列名
    pkt_len_list = df.values.tolist()
    print(pkt_len_list)

    # list转dataframe
    #df = pd.DataFrame(pkt_len_list, columns=['pkt', 'len'])

    # 保存到本地excel
    #df.to_excel("pkt_len.xlsx", index=False)
    xy=np.array(pkt_len_list)
    plt.plot(xy[:,0],xy[:,1],linewidth=1)
    plt.xlabel("pktmun")
    plt.ylabel("len")
    plt.savefig('pcap转png', dpi = 600) 
    plt.show()



def main(file_path, my_ip, dst_ip): #此函数主要是读取pcap文件，再根据IP判断是收包还是发包
    packets=rdpcap(file_path)
    count = 0
    count_dict = {} #创建一个字典将结果保存
    for data in packets:
        try:
            print('------------')
            if data['IP'].dst==my_ip and data['IP'].src==dst_ip :
                print('接收数据包: ', len(data))
                count_dict[-count] = len(data) 
            if data['IP'].dst==dst_ip and data['IP'].src==my_ip:
                print('发送数据包: ', len(data))
                count_dict[count] = len(data)
            print('------------')
            
        except Exception:
            continue
        finally:
            count += 1            
    print(count_dict)
    return count_dict


def Write_excel(count_dict, times): #此函数主要是将数据分析后写入Excel表格
    send_pack_num = 0
    rev_pack_num = 0
    add_send = 0
    add_rev = 0
    all_pack = 0
    timepoint = 0
    f = xlwt.Workbook()
    sheet1 = f.add_sheet('sheet1',cell_overwrite_ok=True)
    row0 = ["时间戳", "总包数量", "发包数量", "发包累计字节数", "收包数量", "收包累计字节数", "总字节数"]
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i])

    for i in range(1, len(count_dict)+1):
        sheet1.write(i, 1, i)
    j = 1
    for (count, packlen) in count_dict.items():
        if count < 0:
            timepoint = times[-count]
            rev_pack_num += 1
            add_rev += packlen
        if count > 0:
            timepoint = times[count]
            send_pack_num += 1
            add_send += packlen
        all_pack = add_send - add_rev
        sheet1.write(j, 0, str(timepoint))
        print(timepoint)
        sheet1.write(j, 2, send_pack_num)
        sheet1.write(j, 3, add_send)
        sheet1.write(j, 4, -rev_pack_num)
        sheet1.write(j, 5, -add_rev)
        sheet1.write(j, 6, all_pack)
        j += 1
    f.save('pcap_analist.xls')
            

def Get_time(file_path):  #此函数主要是为了获取时间戳
    f = open(file_path, mode='rb')  #打开pcap文件
    pcap = dpkt.pcap.Reader(f) #按.pcap格式解析
    times = [] 
    for (ts,buf) in pcap:
        times.append(ts)
    print(times)
    return times
if __name__ == '__main__':
    my_ip = '192.168.1.123'#input('请输入自己的IP')
    baidu_ip = '192.168.1.101'#input ('请输入百度的IP')
    file_path = 'billbill.pcap'#input('请输入pcap格式的文件的路径，斜杠要变成反斜杠')
    count_dict = main(file_path, my_ip, baidu_ip)
    times = Get_time(file_path)
    Write_excel(count_dict=count_dict, times=times)
    excel_line_to_list()
    os.remove("pcap_analist.xls") 
