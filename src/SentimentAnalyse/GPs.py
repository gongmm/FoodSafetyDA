# -*- coding: utf-8 -*-
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

        x = list(x.T[0])

        plt.plot(xs, ym, color=MEANCOLOR, ls='-', marker='None', ms=12, mew=2, lw=3.)
        plt.plot(x, y, color=DATACOLOR, ls='None', marker='+', ms=12, mew=2)
        plt.plot(pre_x, pre_y, color=PRETCOLOR, ls='None', marker='+', ms=12, mew=2)
        plt.plot(p_x, p_y, color=REALDATACOLOR, ls='None', marker='+', ms=12, mew=2)

        plt.show()


class DataPredict():

    def __init__(self):
        self.date, self.hot = self.getDate(month=8)

    def getDate(self, month):
        hot = calculate_fever_by_topic(topic_id=21, month=month)[:10]
        date = [i for i in range(1, 11)]

        return date, hot

    def predict(self, predict_day_num=5):
        # def predict(self):
        print('__date__:', self.date)
        print('__hot__:', self.hot)

        p_y = self.hot[-1]
        p_x = self.date[-1]
        del self.hot[-1]

        day_min = min(self.date)
        # 预测后面五天的数据
        day_max = max(self.date) + predict_day_num

        test_data = []
        while day_min <= day_max:
            test_data.append([day_min])
            day_min = day_min + 1

        train_data = []
        for i in range(0, len(self.date) - 1):
            train_data.append([self.date[i]])

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
