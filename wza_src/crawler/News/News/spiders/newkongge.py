#-*- coding: utf-8 -*-
import io
import os   #读取txt文件所需要的包
import linecache #读取指定行函数linecache.getline(file_ob, line_num)所在的包
import re
import time
import requests

def get_gids():
	root = 'F:\\研-毕业论文\\2018_01_01-2018_12_18+002+1902++_log\\2018_01_01-2018_12_18+002+1902++_log'  # 读取的批量txt所在的文件夹的路径
	file_names = os.listdir(root)  # 读取文件夹下所有的txt的文件名
	file_ob_list = []  # 定义一个列表，用来存放刚才读取的txt文件名
	for file_name in file_names:  # 循环地给这些文件名加上它前面的路径，以得到它的具体路径
		fileob = root + '\\' + file_name  # 文件夹路径加上\\ 再加上具体要读的的txt的文件名就定位到了这个txt
		file_ob_list.append(fileob)  # 将路径追加到列表中存储  ['D:\\project\\kdxf\\data5\\2018_01_01-2018_12_18+002+1902++_log\\2.txt',。。。。]

	print(file_ob_list)  # 打印这个列表的内容到显示屏，不想显示的话可以去掉这句

	line_num = 1  # 从txt的第一行开始读入
	# total_line = len(open(file_ob_list[0]).readlines())  # 计算一个txt中有多少行
	total_line = 20
	while line_num <= total_line:  # 只有读完的行数小于等于总行数时才再读下一行，否则结束读取
		count = 0
		for file_ob in file_ob_list:  # 按顺序循环读取所有文件
			count = count+1
			f = open(file_ob , 'r', encoding='UTF-8')
			for line in f.readlines():
				line1 = line.split()[1]  # 取这一行空格前者
				print (line1)
			# 	while line_num <= total_line:  # 只有读完的行数小于等于总行数时才再读下一行，否则结束读取
			# line = linecache.getline(file_ob, line_num)  # 读取这个文件的第line_num行
			# line1 = line.split()[0]  # 取这一行空格前者
			# line2 = line.split()[1]  # 取这一行空格后者
			# f.write(line2+'\n')  # 创建存放数据的文件

		f.close()

if __name__ == '__main__':
    get_gids()