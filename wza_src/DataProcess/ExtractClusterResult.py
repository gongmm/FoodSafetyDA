import os
import shutil

from sklearn.externals import joblib

vec_dir = 'vec_arr'
cluster_matrix_dir = os.path.join('cluster', 'cluster_matrix')
topic_doc_dir = 'topic_doc'


def get_cluster_result():
    """获得层次聚类后的结果"""
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
    print('————处理第' + topic_index + '个主题————')
    cluster_results = []
    # 存结果矩阵
    cluster_file = os.path.join(cluster_matrix_dir, matrix_file)
    matrix = joblib.load(cluster_file)
    # 存文档索引
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
    # pd_matrix = pd.DataFrame(matrix, columns=['cluster_id'])
    # result_matrix_file = os.path.join(cluster_result_dir, 'topic' + index + '_matrix.csv')
    # pd_matrix.to_csv(result_matrix_file, index=False)

    # pd_index = pd.DataFrame(doc_index)
    # result_index_file = os.path.join(cluster_result_dir, 'topic' + index + '_index.csv')
    # pd_index.to_csv(result_index_file, index=True)

    print('————结束存储结果————')
    return cluster_results


def save_topic_cluster_result(topic_index, cluster_topic_result):
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
