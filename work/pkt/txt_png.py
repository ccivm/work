import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt
def excel_line_to_list():
    df = pd.read_table("billbill.txt", sep=',',names=None,header=None)  # 读取两列，并不要列名
    pkt_len_list = df.values.tolist()
    print(pkt_len_list)
    x=0
    for x in range(len(pkt_len_list)):
    	a=int(pkt_len_list[x-1][1])
    	pkt_len_list[x-1][1]=-a
    xy=np.array(pkt_len_list)
    plt.plot(xy[:,0],xy[:,1],linewidth=1)
    plt.xlabel("pktmun")
    plt.ylabel("len")
    plt.savefig('pcap转png', dpi = 600) 
    plt.show()

if __name__ == '__main__':
    excel_line_to_list()

