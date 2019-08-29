# -*- coding: utf-8 -*-
import csv

import pyGPs
import numpy as np
import matplotlib.pyplot as plt

from sentiment_fever_day import calculate_fever_by_topic

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体

plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

SHADEDCOLOR = [0.7539, 0.89453125, 0.62890625, 1.0]
MEANCOLOR = [0.2109375, 0.63385, 0.1796875, 1.0]
DATACOLOR = [0.12109375, 0.46875, 1., 1.0]
REALDATACOLOR = [0.46875, 0.12109375, 0.62890625, 1.0]
PRETCOLOR = [1.0, 0.2, 0.7539, 1.0]


class GPRY(pyGPs.GPR):
    def draw_figure(self, p_x, p_y, axisvals=None):
        """
        Plot 1d GP regression result.
        :param list axisvals: [min_x, max_x, min_y, max_y] setting the plot range
        """
        xs = self.xs  # test point
        x = self.x
        y = self.y
        ym = self.ym  # predictive test mean
        lp = self.lp
        pre_x = []
        pre_y = []
        index = x[-1][0] + 1
        for i in range(len(xs)):
            # print xs[i][0]
            if int(xs[i][0] + 0.1) == index:
                pre_x.append([xs[i][0]])
                pre_y.append([ym[i][0]])
                index = index + 1

        print(str(pre_y))
        print(lp)

        x = list(x.T[0])

        plt.plot(xs, ym, color=MEANCOLOR, ls='-', marker='None', ms=12, mew=2, lw=3.)
        plt.plot(x, y, color=DATACOLOR, ls='None', marker='+', ms=12, mew=2)
        plt.plot(pre_x, pre_y, color=PRETCOLOR, ls='None', marker='+', ms=12, mew=2)
        plt.plot(p_x, p_y, color=REALDATACOLOR, ls='None', marker='+', ms=12, mew=2)
        # 保存图片
        plt.savefig('result/trend_prediction.png', bbox_inches='tight')
        plt.show()
        # 将数据保存为csv
        headers = ['x_value', 'origin_data', 'mean_data']
        with open('result/trend_prediction_data.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for index, x_value in enumerate(x):
                writer.writerow([x_value, y[index][0], ym[index][0]])


class DataPredict:

    def __init__(self):
        self.date, self.hot = self.get_date_fever(month=8)

    @staticmethod
    def get_date_fever(month):
        hot = calculate_fever_by_topic(topic_id=21, month=month)
        days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        date = [i for i in range(1, days[month - 1] + 1)]

        return date, hot

    def predict(self, predict_day_num=1, use_day_num=30):
        print('__date__:', self.date)
        print('__hot__:', self.hot)

        p_y = self.hot[use_day_num:][:predict_day_num]
        p_x = self.date[use_day_num:][:predict_day_num]
        self.hot = self.hot[:use_day_num]
        self.date = self.date[:use_day_num]

        day_min = min(self.date)
        # 预测后面五天的数据
        day_max = max(self.date) + predict_day_num

        test_data = []
        while day_min <= day_max:
            test_data.append([day_min])
            day_min = day_min + 1

        train_data = self.date
        # for i in range(0, len(self.date) - 1):
        #     train_data.append([self.date[i]])

        train_data = np.array(train_data)
        self.hot = np.array(self.hot)
        test_data = np.array(test_data)

        x = train_data  # training data
        y = self.hot  # training target
        z = test_data  # test data
        print(x)
        print(y)
        print(z)

        model = GPRY()  # specify model (GP regression)
        model.getPosterior(x, y)  # fit default model (mean zero & rbf kernel) with data
        model.optimize(x, y)  # optimize hyperparamters (default optimizer: single run minimize)

        model.predict(z)
        model.draw_figure(p_x, p_y)


if __name__ == '__main__':
    class_predict = DataPredict()
    class_predict.predict()
