import os
import numpy as np
from sklearn.externals import joblib
import matplotlib.pylab as plt
from state_transition import get_all_state_transition
# from sentiment_fever import calculate_fever_by_topic
from sentiment_fever_day import calculate_fever_by_topic

result_dir = 'result'
if not os.path.exists(result_dir):
    os.makedirs(result_dir)


# main functions
def trend_predict(total_list):
    """根据所有主题/事件的热度值进行趋势预测并将预测的状态存入文件中

    Args:
        total_list: 二维列表，所有主题/事件的热度值列表。
        第一维表示每个主题/事件的热度值列表，第二维表示每个月的热度值。
    """
    state_file = os.path.join(result_dir, 'states')
    matrix_list, init_state_list = get_all_state_transition(total_list)
    states_list = []
    for i in range(len(matrix_list)):
        n = len(total_list[i])-1
        states = predict_state(matrix_list[i], init_state_list[i], n)
        states_list.append(states)
    joblib.dump(states_list, state_file)


def analyse_result(state_file):
    """分析所有主题/事件的状态并画出趋势图
    Args:
        state_file: 存放状态列表的文件路径
    """
    states_vec_list = joblib.load(state_file)
    for i in range(len(states_vec_list)):
        state_indice = get_state_index(states_vec_list[i])
        file = os.path.join(result_dir, 'topic' + str(i) + '_trend.png')
        plot_states(state_indice, file)


# internal functions
def predict_state(matrix, init_state, n):
    """根据状态转移概率矩阵和初始状态求出每个月的状态向量

    Args:
        matrix: 状态转移概率矩阵
        init_state: 初始状态

    Returns:
        states: 状态向量列表
    """
    states = []
    state = init_state
    # state = np.array([0, 1, 0, 0])
    for i in range(1, n):
        # matrix_power = np.power(matrix, i)
        state = np.matmul(state, matrix)
        states.append(state)
    return states


def get_state_index(states_vec):
    """根据状态概率向量求状态值

    取概率最大的状态作为预测状态。
    状态值从1开始，但在向量中存放位置是从0开始，所以要+1。

    Args:
        states_vec: 状态概率向量列表，位置i表示状态S_i+1的概率。

    Returns:
        state_indice: 状态值列表
    """
    state_indice = []
    for state_vec in states_vec:
        state_index = np.argmax(state_vec)+1
        state_indice.append(state_index)
    return state_indice


def plot_states(state_indice, file):
    """根据状态值画出趋势图

    Args:
        state_indice: 状态值列表
        file: 画图存放的文件路径
    """
    trend_values = get_trend_value(state_indice)
    n = len(state_indice)
    x = [i for i in range(1, n+2)]
    plt.plot(x, trend_values)
    plt.xlabel('Month')
    plt.ylabel('trend value')
    plt.title('trend analysis for topic')
    plt.xticks([i for i in range(1, n+1)])
    plt.yticks([2*i for i in range(5)])
    plt.savefig(file)


def get_trend_value(state_indice):
    """为状态值列表定义一系列对应的趋势值便于画图

    Args:
        state_indice: 状态值列表

    Returns:
        trend_values: 趋势值列表
    """
    cur_value = 2
    trend_values = [cur_value]  # 初始值
    for state in state_indice:
        k = get_state_slope(state)
        cur_value += k
        trend_values.append(cur_value)
    return trend_values


def get_state_slope(state_index):
    """获得状态值的增长斜率

    Args:
        state_index: 状态值

    Returns: 增长斜率
    """
    if state_index == 1:
        return 2
    if state_index == 2:
        return 0.5
    if state_index == 3:
        return -0.5
    return -2  # state_index == 4


if __name__ == '__main__':
    # year
    # topic_list = calculate_fever_by_topic(topic_id=21)
    topic_list = calculate_fever_by_topic(topic_id=21, month=2)[:20]
    #topic_list = [46.52, 97.56, 139.52, 128.84, 156.78, 108.92, 81.08, 49.02, 45.4, 50.81, 71.8, 36.52, 38.08, 44.68,
     #             51.6, 61.56, 36, 51.8]
    # month
    total_list = [topic_list]
    trend_predict(total_list)
    state_file = os.path.join(result_dir, 'states')
    analyse_result(state_file)