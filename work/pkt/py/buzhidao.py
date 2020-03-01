import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt
def excel_line_to_list():
    df = pd.read_excel("090201.xlsx", usecols=[1, 6],names=None)  # 读取两列，并不要列名
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
    plt.savefig('pkt_len_list1', dpi = 600) 
    plt.show()

if __name__ == '__main__':
    excel_line_to_list()