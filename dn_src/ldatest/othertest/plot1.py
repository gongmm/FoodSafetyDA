#-*- coding:utf-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams["font.sans-serif"]=["SimHei"]
mpl.rcParams['axes.unicode_minus']=False

#x=[1,2,3,4,5]
y=[85,172,260,38,135]
x=['猪肉牛肉检疫','超市月饼过期','疫情非洲猪瘟','大闸蟹阳澄湖螃蟹','中毒症状医院']
wendang=[85,172,260,38,135]
# 设置Y轴的刻度范围
plt.xlim([0,300])
plt.barh(x,y,align='center',color="lightskyblue")
# 为每个条形图添加数值标签    enumerate可以同时获得索引和值
for x,y in enumerate(wendang):
    plt.text(y+10,x,'%s' %y,ha='center')
plt.ylabel("主题")
plt.xlabel("文档数")

#plt.grid(True,axis='y',ls=":",color='r',alpha=0.3)
plt.show()