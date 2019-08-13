import numpy as np

STATE_NUM = 4


# main functions
def get_all_state_transition(total_list):
    """根据所有主题/事件的热度值计算状态转移概率矩阵和初始状态

    Args:
        total_list: 二维列表，所有主题/事件的热度值列表。
        第一维表示每个主题/事件的热度值列表，第二维表示每个月的热度值。

    Returns:
        matrix_list: 状态转移概率矩阵列表
        init_state_list: 初始状态列表
    """
    matrix_list = []
    init_state_list = []
    for hot_list in total_list:
        matrix, init_state_vec = state_transit(hot_list)
        matrix_list.append(matrix)
        init_state_list.append(init_state_vec)

    return matrix_list, init_state_list


# internal functions
def state_transit(hot_list):
    """计算一个事件/主题的状态转移，得到状态转移概率矩阵

    Args:
        hot_list: 一个事件/主题的按时间序列的热度值列表

    Returns:
        matrix: 状态转移概率矩阵
        init_state_vec: 初始状态向量
    """
    # 计算热度趋势值
    trend_list = []
    for i in range(len(hot_list)-1):
        t = hot_list[i+1] - hot_list[i]
        trend_list.append(t)

    # 构造状态区间
    state_interval = get_state_interval(trend_list)

    # 构造状态转移表
    table, init_state_vec = get_transit_table(trend_list, state_interval)

    # 构造状态转移概率矩阵
    matrix = get_transit_prob_matrix(table)

    return matrix, init_state_vec


def get_transit_table(trend_list, interval):
    """构造状态转移表

    状态转移表是一个NxN的矩阵，N为定义的状态个数。

    n_ij，行索引i表示当前状态，列索引j表示下一刻状态，
    元素n_ij的值：表示当前状态为S_i，下一刻S_j的有n_ij个。
    如果初始热度x1处于状态S1，初始状态向量表示为(1,0,0,0)。

    Args:
        trend_list: 热度趋势值列表
        interval: 元组，状态区间

    Returns:
        table: 状态转移表
        init_state_vec: 初始状态向量
    """
    n = len(trend_list)
    table = np.zeros((STATE_NUM, STATE_NUM), dtype=np.int)
    init_state_vec = None
    for i in range(n-1):
        cur_state = get_state(trend_list[i], interval)
        next_state = get_state(trend_list[i+1], interval)
        table[cur_state][next_state] += 1
        # 构造初始状态向量
        if i == 0:
            init_state_vec = np.zeros(STATE_NUM, dtype=np.int)
            init_state_vec[cur_state] = 1
    return table, init_state_vec


def get_state(trend, interval):
    """ 计算指定趋势值所在状态区间

    S1 = [t_max/2, t_max]
    S2 = [0, t_max/2]
    S3 = [t_min/2, 0]
    S4 = [t_min, t_min/2] (t_min<0)
    元组间两个连续的元素构成一个区间。

    Args:
        trend: 热度趋势值
        interval: 元组，状态区间 (t_min, t_half_min, 0, t_half_max, t_max)

    Returns: 整数，状态区间的标号-1，用于后续状态转移表的下标索引
    """
    if interval[0] <= trend < interval[1]:
        return 4-1
    if interval[1] <= trend < interval[2]:
        return 3-1
    if interval[2] <= trend < interval[3]:
        return 2-1
    return 1-1  # interval[3] <= trend < trend[4]


def get_state_interval(trend_list):
    """划分状态区间

    S1 = [t_max/2, t_max]
    S2 = [0, t_max/2]
    S3 = [t_min/2, 0]
    S4 = [t_min, t_min/2] (t_min<0)

    Args:
        trend_list: 热度趋势列表

    Returns:
        state_interval: 元组，元组间两个连续的元素构成一个区间
    """
    t_max = max(trend_list)
    t_min = min(trend_list)
    t_half_max = t_max / 2
    t_half_min = t_min / 2
    state_interval = (t_min, t_half_min, 0, t_half_max, t_max)
    return state_interval


def get_transit_prob_matrix(table):
    """构造状态转移概率矩阵

    首先求当前状态为S_i的总和，即一行的所有列相加，sum_j(n_ij)。
    然后用频率代表概率，p_ij = n_ij/sum_j(n_ij)。

    col_sum为1xN矩阵, 将其转置为Nx1的矩阵。

    Args:
        table: 构造状态转移表

    Returns:
        matrix: 状态转移概率矩阵
    """
    col_sum = table.sum(axis=1)  # 计算每行的总和(一行的所有列相加)， col_sum为1xN矩阵

    # 避免除数为0，将sum为0的设置为1，0/1还是0，不影响最后运算结果
    for i in range(len(col_sum)):
        if col_sum[i] == 0:
            col_sum[i] = 1

    # col_sum为1xN矩阵, 将其转置为Nx1的矩阵
    col_sum.shape = (STATE_NUM, 1)

    matrix = np.divide(table, col_sum)  # 利用np广播的特性，每行除以同一个数
    return matrix
