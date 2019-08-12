import numpy as np
import math
import pandas as pd

# 原始数据
from sentiment_fever import calculate_fever_by_topic

data = calculate_fever_by_topic(topic_id=21)[:7]

n = len(data)
x0 = np.array(data)

# 级比检验
lmda = [data[i - 1] / data[i] for i in range(1, n)]
lmda = np.array(lmda)

# 累加生成
sum_data = [sum(data[0:i + 1]) for i in range(n)]
x1 = np.array(sum_data)

# 计算数据矩阵B和数据向量Y
B = np.zeros([n - 1, 2])
Y = np.zeros([n - 1, 1])
for i in range(n - 1):
    B[i][0] = -0.5 * (x1[i] + x1[i + 1])
    B[i][1] = 1
    Y[i][0] = x0[i + 1]

# 计算GM(1,1)微分方程的参数a和b
A = np.zeros([2, 1])
B_ = B.T
A = np.linalg.inv(B_.dot(B)).dot(B_).dot(Y)
a = A[0][0]
b = A[1][0]

# 建立灰色预测模型
xx0 = np.zeros(n)
xx0[0] = x0[0]
for i in range(1, n):
    xx0[i] = (x0[0] - b / a) * math.exp(-a * i) * (1 - math.exp(a))
print('预测出的数据为：\n', xx0)

# 进行残差检验
# 求残差平均值
e = 0
for i in range(n):
    e += (x0[i] - xx0[i])
e /= n
print('残差平均值为：', e)
# 求历史数据平均值
avg = 0
for i in range(n):
    avg += x0[i]
avg /= n
# 求历史数据方差
s1 = 0
for i in range(n):
    s1 += (x0[i] - avg) ** 2
s1 /= n
# 求残差方差
s2 = 0
for i in range(n):
    s2 += (x0[i] - xx0[i] - e) ** 2
s2 /= n
# 求后验差比值
C = s2 / s1
print('后验差比值为：', C)
# 求小误差概率
cout = 0
for i in range(0, n):
    if abs((x0[i] - xx0[i]) - e) < 0.6754 * math.sqrt(s1):
        cout = cout + 1
P = cout / n
print('小误差概率为：', P)

# 进行预测
can_predict = False
level = 0
if C < 0.35 and P > 0.6:
    can_predict = True
    if P > 0.95:
        level = 1
    elif P > 0.85:
        level = 2
    elif P > 0.7:
        level = 3
    else:
        level = 4

if can_predict is True:
    print('可以采用灰度预测模型，模型预测准确度等级为：', level)
    m = int(input('请输入需要预测的年数:'))
    print('往后%d年预测值依次为：' % m)
    predict = np.zeros(m)
    for i in range(m):
        predict[i] = (x0[0] - b / a) * (1 - math.exp(a)) * math.exp(-a * (i + n))
    print(predict)
else:
    if C > 0.35:
        print('后验差比值>0.35')
    elif P < 0.6:
        print('小误差概率<0.6')
    print('灰色预测法不适用')
