# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 14:05:35 2017

@author: HBB
"""

# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# 这里导入你自己的数据
# ......
# ......
# x_axix，train_pn_dis这些都是长度相同的list()

# 开始画图
sub_axix = filter(lambda x: x % 200 == 0, x_axix)
plt.title('Result Analysis')
plt.plot(x_axix, train_acys, color='green', label='training accuracy')
plt.plot(sub_axix, test_acys, color='red', label='testing accuracy')
plt.plot(x_axix, train_pn_dis, color='skyblue', label='PN distance')
plt.plot(x_axix, thresholds, color='blue', label='threshold')
plt.legend()  # 显示图例

plt.xlabel('iteration times')
plt.ylabel('rate')
plt.show()
# python 一个折线图绘制多个曲线