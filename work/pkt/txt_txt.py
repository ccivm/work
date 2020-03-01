import pandas as pd
import numpy as np  
import matplotlib.pyplot as plt
import os  

def excel_line_to_list():
	df = pd.read_table("22470bilibili.txt", sep=' ',names=None,header=None,index_col=None,)  # 读取两列，并不要列名
	print(df)
	x=0
	y=0
	i=0
	m=[]
	n=[]
	for y in range(len(df)):
		a=y+1#int(df[x][y])
		m.append(a)
	x=1
	for y in range(len(df)):
		a=1-int(df[x][y])
		n.append(a)
	f=open('billbill.txt', 'w')
	print(len(n))
	for i in range(0,len(m)):
		f.write(str(m[i]))
		f.write(',')
		f.write(str(n[i]))
		f.write('\n')
	f.close()

	# path=os.getcwd()
	# df.to_csv('billbill.txt',header=0,index=0)


if __name__ == '__main__':
    excel_line_to_list()
