import os
import shutil

from sklearn.externals import joblib

vec_dir = 'vec_arr'
cluster_matrix_dir = os.path.join('cluster', 'cluster_matrix')
topic_doc_dir = 'topic_doc'


def get_cluster_result():
    """
    获得层次聚类后的结果
    Returns:

    """
    print('————开始存储结果————')
    cluster_result_dir = os.path.join('cluster', 'result')
    is_exists = os.path.exists(cluster_result_dir)
    if not is_exists:
        os.makedirs(cluster_result_dir)
    matrix_files = os.listdir(cluster_matrix_dir)
    for matrix_file in matrix_files:
        topic_index = matrix_file[5:-7]
        cluster_topic_result = get_cluster_topic_result(matrix_file, topic_index)
        save_topic_cluster_result(topic_index, cluster_topic_result)


def get_cluster_topic_result(matrix_file, topic_index):
    """
    获得某个主题的聚类结果
    Args:
        matrix_file: 矩阵文件名
        topic_index: 处理的话题号

    Returns:
        主题中各个事件包括的文档名，二维链表(event_number, doc_number)
    """
    print('————处理第' + topic_index + '个主题————')
    cluster_results = []
    # 结果矩阵
    cluster_file = os.path.join(cluster_matrix_dir, matrix_file)
    matrix = joblib.load(cluster_file)
    # 文档索引
    doc_id_file = os.path.join(vec_dir, 'topic' + topic_index + '_doc.index')
    doc_index = joblib.load(doc_id_file)
    # 聚类个数
    cluster_num = max(matrix)
    for i in range(1, cluster_num + 1):
        cluster_result = []
        indexes = [key for key, value in enumerate(matrix.tolist()) if value == i]
        for index in indexes:
            doc_num = doc_index[index]
            doc_name = 'topic' + topic_index + '_doc' + str(doc_num) + '.txt'
            cluster_result.append(doc_name)
        cluster_results.append(cluster_result)
    print('————结束存储结果————')
    return cluster_results


def save_topic_cluster_result(topic_index, cluster_topic_result):
    """
    保存聚类结果，将主题下的文档按照事件分类存储 topic_i/events/event_j/doc...
    Args:
        topic_index: 处理的话题号
        cluster_topic_result: 主题的聚类结果

    Returns:

    """
    topic_dir = os.path.join(topic_doc_dir, 'topic' + topic_index)
    # 如果不存在则创建目录
    if not os.path.exists(topic_dir):
        os.makedirs(topic_dir)
    events_dir = os.path.join(topic_dir, 'events')
    # 如果不存在则创建目录
    if not os.path.exists(events_dir):
        os.makedirs(events_dir)

    for event_index, event_docs in enumerate(cluster_topic_result):
        event_dir = os.path.join(events_dir, 'event' + str(event_index))
        # 如果不存在则创建目录
        if not os.path.exists(event_dir):
            os.makedirs(event_dir)
        for doc in event_docs:
            src_dir = os.path.join(topic_dir, doc)
            dest_dir = os.path.join(event_dir, doc)
            shutil.copyfile(src_dir, dest_dir)


if __name__ == '__main__':
    get_cluster_result()
