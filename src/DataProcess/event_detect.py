import os

import numpy as np
from sklearn.externals import joblib
from scipy.cluster import hierarchy  # 用于进行层次聚类，画层次聚类图的工具包
import matplotlib.pylab as plt
import warnings

from doc_2_vec import train_model
from doc_2_vec import doc2vec
from doc_2_vec import entity2vec
from event_util import get_topic_doc
from event_util import get_doc_entity


warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

result_dir = 'result'
model_dir = 'model'
vec_dir = 'vec_arr'
corpus_dir = 'corpus'
cluster_matrix_dir = os.path.join('cluster', 'cluster_matrix')
cluster_plot_dir = os.path.join('cluster', 'cluster_plot')


def similarity(a_vect, b_vect):
    """ 计算两个向量的余弦相似度

    Args:
        a_vect: a 向量
        b_vect: b 向量

    Returns:
        cos: 余弦相似度
    """
    # dot_val = 0.0
    # a_norm = 0.0
    # b_norm = 0.0
    # cos = None
    # for a, b in zip(a_vect, b_vect):
    #     dot_val += a * b
    #     a_norm += a ** 2
    #     b_norm += b ** 2
    # if a_norm == 0.0 or b_norm == 0.0:
    #     cos = -1
    # else:
    #     cos = dot_val / ((a_norm * b_norm) ** 0.5)

    sim = np.sqrt(((a_vect - b_vect) ** 2).sum())
    return sim


def get_doc_similarity(d1, d2):
    """计算文档d1与d2的相似度

    Args:
        d1: 文档d1向量
        d2: 文档d2向量

    Returns:
        sim_doc: 余弦相似度
    """
    return similarity(d1, d2)


def get_entity_similarity(entity_1, entity_2):
    """计算命名实体序列向量间的相似度

    Args:
        entity_1: 命名实体序列向量1
        entity_2: 命名实体序列向量2

    Returns:
        sim_entity: 余弦相似度
    """
    return similarity(entity_1, entity_2)


def get_distance(d1, d2):
    """获得加权的总相似度

    Sim(d1, d2) = w * Sim_doc(d1, d2) + (1-w) * Sim_entity(d1, d2)
    d1，d2为两个不同的文档；
    w为文档相似度的权重，需要实验得出；
    Sim_doc(d1, d2)计算文档相似度
    Sim_entity(d1, d2)计算文档中提取的命名实体序列的相似度

    Args:
        d1: 文档1的向量
        d2: 文档2的向量
        (注意: 0-255维是文档向量，256-306维是命名实体序列向量)

    Returns:
        sim: 加权相似度，作为层次聚类的距离值
    """
    sim_doc = get_doc_similarity(d1[:256], d2[:256])
    sim_entity = get_entity_similarity(d1[256:], d2[256:])

    w = 0.7  # weight
    sim = w * sim_doc + (1 - w) * sim_entity
    return sim


def hierarchy_cluster(topic_num):
    """对每个主题下的所有文档进行层次聚类

    Args:
        topic_num: 主题数量
    """
    for i in range(topic_num):
        print('————处理第%d个主题————' % i)

        # 加载文档向量文件
        is_exists = os.path.exists(vec_dir)
        if not is_exists:
            os.makedirs(vec_dir)
        vec_file = os.path.join(vec_dir, 'topic' + str(i) + '.vec')

        vec_arr = joblib.load(vec_file)

        Z = hierarchy.linkage(vec_arr, method='weighted', metric=get_distance)
        # 根据距离阈值确定文档的聚类结果
        matrix = hierarchy.fcluster(Z, t=0.5, criterion='distance')
        # 存储聚类结果图片
        is_exists = os.path.exists(cluster_plot_dir)
        if not is_exists:
            os.makedirs(cluster_plot_dir)
        plot_file = os.path.join(cluster_plot_dir, 'topic' + str(i) + '_dendrogram.png')
        hierarchy.dendrogram(Z)  # 画图：聚类结果
        plt.savefig(plot_file)  # 存储聚类结果图片

        # 写入聚类结果文件
        is_exists = os.path.exists(cluster_matrix_dir)
        if not is_exists:
            os.makedirs(cluster_matrix_dir)
        cluster_file = os.path.join(cluster_matrix_dir, 'topic' + str(i) + '.matrix')
        joblib.dump(matrix, cluster_file)


def events_detect():
    print("———————————开始提取事件—————————————")

    print("———开始整理主题文档———")
    # topic_num = get_topic_doc()
    topic_num = 45
    print("———结束整理主题文档———")

    print("———开始获得命名实体———")
    # get_doc_entity(topic_num)
    print("———结束获得命名实体———")

    print("—————开始训练模型—————")
    # train_model(topic_num)
    print("—————结束训练模型—————")

    print("————开始文档向量化————")
    # doc2vec(topic_num)
    print("————结束文档向量化————")

    print("————开始实体向量化————")
    # entity2vec(topic_num)
    print("————结束实体向量化————")

    print("—————开始层次聚类—————")
    hierarchy_cluster(topic_num)
    print("—————结束层次聚类—————")

    print("—————————————结束提取事件———————————")


if __name__ == '__main__':
    events_detect()
