import os
import gensim
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from scipy.cluster import hierarchy  # 用于进行层次聚类，画层次聚类图的工具包
import matplotlib.pylab as plt
import re
import warnings
import pickle
import tensorflow as tf
import jieba


import sys
sys.path.append('..')  # 添加自己指定的搜索路径
sys.path.append('../ChineseNER')
from ChineseNER.model import Model
import ChineseNER.loader
import ChineseNER.utils
import ChineseNER.data_utils

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

result_dir = 'result'
model_dir = 'model'
vec_dir = 'vec_arr'
corpus_dir = 'corpus'
cluster_matrix_dir = os.path.join('cluster', 'cluster_matrix')
cluster_plot_dir = os.path.join('cluster', 'cluster_plot')
# 主题id-词文件，格式：[主题id, 词]
topic_word_csv = os.path.join(result_dir, 'food_topic_word.csv')
# 文档信息-主题id文件，格式：[文档信息, 主题id]
news_data_topic_csv = os.path.join(result_dir, 'all_news_data_utf_topic.csv')
# 文档id-主题id文件，格式：[文档id, 主题id]
doc_topic_csv = os.path.join(result_dir, 'doc_topic.csv')


def get_topic_doc():
    """将同一个主题的所有文档整理到相同文件夹中

    读取文档信息-主题id文件，对于每一个文档，将其内容写入对应的主题文件夹的txt文件中。
    """

    # 获得主题数
    topic_df = pd.read_csv(topic_word_csv)
    topic_num = topic_df.shape[0]

    # 将同一个主题的文档写入同一个文件夹的不同txt文件中
    # news_topic_df = pd.read_csv(news_data_topic_csv)
    doc_topic_df = pd.read_csv(doc_topic_csv)
    doc_num = doc_topic_df.shape[0]

    corpus_path = os.path.join(corpus_dir, 'news_content_corpus.txt')
    with open(corpus_path, 'r', encoding='utf-8') as f:
        doc_word_list = f.readlines()

    for i in range(doc_num):
        print('处理第%d个文档' % (i+1))
        # 判断文档对应的主题文件夹是否存在
        # content, title, topic_id = news_topic_df.loc[i, ['content', 'title', 'topic_id']]
        topic_id = doc_topic_df.loc[i, 'topic_id']

        line = doc_word_list[i]

        topic_dir = 'topic_doc/topic' + str(topic_id)
        is_exists = os.path.exists(topic_dir)
        # 如果不存在则创建目录
        if not is_exists:
            os.makedirs(topic_dir)

        file_path = 'topic_doc/topic' + str(topic_id) + \
                    '/topic' + str(topic_id) + '_doc' + str(i+1) + '.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            # 写入文件
            # print(line)
            f.write(line + '\n')  # 把这行写进文件

    return topic_num


def get_doc_entity(topic_num):
    """调用ChineseNER获得所有文档的命名实体

    获得所有文档的命名实体，将去重后的实体当成是分词，后续要送入doc2vec模型中训练。

    Args:
        topic_num: 主题的数量
    """

    with open('data/regular_total/news_content.txt', 'r', encoding='utf-8') as f:
        doc_contents = f.readlines()  # 一行文本
    for i in range(topic_num):
        print('————处理第%d个主题————' % i)
        # 读取一个主题中所有文档的文件名
        topic_dir = "topic_doc/topic" + str(i)
        doc_labels = [f for f in os.listdir(topic_dir) if f.endswith('.txt')]

        for doc_file in doc_labels:
            pattern = re.compile('doc\\d+')
            result = re.search(pattern, doc_file)
            if result:
                doc_id = result.group()[3:]  # 根据文件名获得文档id
                # 获得预处理后的文本
                content = doc_contents[int(doc_id)]

                # 送入ChineseNER模型中得到命名实体
                line = evaluate_entities(content)

                entity_dir = os.path.join('topic_doc', 'topic' + str(i), 'entity')
                is_exists = os.path.exists(entity_dir)
                if not is_exists:
                    os.makedirs(entity_dir)
                file_path = os.path.join(entity_dir, 'topic' + str(i) + '_entity' + str(doc_id) + '.txt')
                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(line + '\n')  # 把命名实体写进文件
            else:
                print('找不到文档文件！')


def train_model(topic_num):
    """ 训练Doc2Vec，并保存模型

    读取每个主题下的所有文档，对于每个主题训练一个Doc2Vec模型。
    变量doc_labels是一个列表，存放对应主题文件夹下所有文档的文件名。

    Args:
        topic_num: 主题的数量

    """
    for i in range(topic_num):
        print('处理第%d个主题' % i)
        # 读取一个主题中所有文档的文件名
        data_dir = "topic_doc/topic" + str(i)
        doc_labels = [f for f in os.listdir(data_dir) if f.endswith('.txt')]

        # 存储一个主题下所有文档内容
        data = []
        for doc in doc_labels:
            ws = open(data_dir + "/" + doc, 'r', encoding='UTF-8').read()
            data.append(ws)
        print(len(data))

        # 创建迭代器
        sentences = LabeledLineSentence(data, doc_labels)

        # 创建模型
        model = gensim.models.Doc2Vec(vector_size=256, window=8, min_count=3,
                                      workers=4, alpha=0.025, min_alpha=0.025, epochs=12)
        # 建立词典
        model.build_vocab(sentences)
        print("开始训练...")

        # 训练模型
        model.train(sentences, total_examples=model.corpus_count, epochs=12)

        # 保存模型
        is_exists = os.path.exists(model_dir)
        if not is_exists:
            os.makedirs(model_dir)
        model_path = os.path.join(model_dir, "doc2vec" + str(i) + ".model")
        model.save(model_path)
        print("model saved")


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


def sent2vec(model, words):
    """ 文本转换成向量

    Args:
        model: Doc2Vec模型
        words: 分词后的文本list

    Returns:
        向量数组
    """
    vect_list = []
    for w in words:
        try:
            vect_list.append(model.wv[w])
        except Exception as e:
            print(e)
            continue
    vect_list = np.array(vect_list)
    vect = vect_list.sum(axis=0)
    return vect / np.sqrt((vect ** 2).sum())


class LabeledLineSentence(object):
    """创建迭代器"""
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield gensim.models.doc2vec.LabeledSentence(words=doc.split(), tags=[self.labels_list[idx]])


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


def sort_key(s):
    if s:
        try:
            c = re.findall('\d+', s)[1]
        except:
            c = -1
        return int(c)


def doc2vec(topic_num):
    """将所有文档转换为向量，并将向量矩阵和文档索引存入对应主题的文件中

    Args:
        topic_num: 主题数量
    """
    for i in range(topic_num):
        print('————处理第%d个主题————' % i)
        print("load model")
        model_path = os.path.join(model_dir, "doc2vec" + str(i) + ".model")
        model = gensim.models.Doc2Vec.load(model_path)

        data_dir = "topic_doc/topic" + str(i)
        doc_labels = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
        doc_labels.sort(key=sort_key)
        print(len(doc_labels))

        is_exists = os.path.exists(vec_dir)
        if not is_exists:
            os.makedirs(vec_dir)
        vec_file = os.path.join(vec_dir, 'topic' + str(i) + '.vec')
        doc_id_file = os.path.join(vec_dir, 'topic' + str(i) + '_doc.index')
        vec_arr = []
        doc_id_list = []

        for j in range(len(doc_labels)):
            doc_file = os.path.join(data_dir, doc_labels[j])
            line = open(doc_file, 'r', encoding='UTF-8').read()  # 一行文件
            words = line.split()

            # 转成句子向量
            vec = sent2vec(model, words)
            vec_arr.append(vec)

            # 得到doc_id
            doc_id = doc_labels[j].split('doc')[1].split('.')[0]
            doc_id_list.append(doc_id)

        joblib.dump(vec_arr, vec_file)
        joblib.dump(doc_id_list, doc_id_file)


def entity2vec(topic_num):
    """将所有文档的命名实体转换为向量

        将得到的命名实体转化为向量，将向量插入文本向量后面，一起构成进行层次聚类所需要的矩阵。
        Args:
            topic_num: 主题数量
        """
    for i in range(topic_num):
        print('————处理第%d个主题————' % i)
        print("load model")

        # 加载word2vec模型
        word2vec_model_file_50 = 'model/word2vec_50.model'
        model = gensim.models.word2vec.Word2Vec.load(word2vec_model_file_50)

        data_dir = os.path.join("topic_doc", "topic" + str(i), "entity")
        entity_labels = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
        entity_labels.sort(key=sort_key)
        print(len(entity_labels))

        vec_file = os.path.join(vec_dir, 'topic' + str(i) + '.vec')
        old_vec_arr = joblib.load(vec_file)
        vec_arr = []

        for j in range(len(entity_labels)):
            doc_file = os.path.join(data_dir, entity_labels[j])
            line = open(doc_file, 'r', encoding='UTF-8').read()  # 一行文件
            words = ''.join(line.split())

            # 分词
            row_list = [eachWord for eachWord in jieba.cut(words)]

            # 去停用词
            out_str = ''
            stop_words = open('corpus/NER_stopwords.txt', 'r', encoding='utf-8').readlines()
            for i in range(len(stop_words)):
                stop_words[i] = stop_words[i].strip()
            for row in row_list:
                if row not in stop_words:
                    if row != '\t':
                        out_str += row
                        out_str += ' '
            words = out_str.split()
            # 转成句子向量
            vec = sent2vec(model, words)
            # 若没有命名实体，命名实体向量填充为0
            if not isinstance(vec, np.ndarray):
                vec = np.zeros(50)
            # 拼接向量
            new_arr = np.concatenate((old_vec_arr[j], vec), axis=0)
            vec_arr.append(new_arr)

        # 写回矩阵文件
        joblib.dump(vec_arr, vec_file)


def hierarchy_cluster(topic_num):
    """对每个主题下的所有文档进行层次聚类

    Args:
        topic_num: 主题数量
    """
    for i in range(2, 3):
        print('————处理第%d个主题————' % i)

        # 加载文档向量文件
        is_exists = os.path.exists(vec_dir)
        if not is_exists:
            os.makedirs(vec_dir)
        vec_file = os.path.join(vec_dir, 'topic' + str(i) + '.vec')

        vec_arr = joblib.load(vec_file)

        Z = hierarchy.linkage(vec_arr, method='weighted', metric=get_distance)
        # 根据距离阈值确定文档的聚类结果
        matrix = hierarchy.fcluster(Z, t=1, criterion='distance')
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


def evaluate_entities(line):
    """获得包含食品专有名词和其他命名实体的文本序列

    Args:
        line: 预处理后的文档文本

    Returns:
        result: 带有命名实体的文本序列
    """
    # 重置默认图形，解决跑两次模型变量已经存在的问题
    tf.reset_default_graph()

    # food entities
    config_file = '../ChineseNER/food/config_file'
    log_file = '../ChineseNER/food/train.log'
    map_file = '../ChineseNER/food/maps.pkl'
    ckpt_path = '../ChineseNER/food/ckpt'
    food_result = evaluate_entities_core(line, config_file, log_file, map_file, ckpt_path)

    food_entities = list(set([f['word'] for f in food_result['entities']]))

    # 重置默认图形，解决跑两次模型变量已经存在的问题
    tf.reset_default_graph()

    # other entities
    config_file = '../ChineseNER/other/config_file'
    log_file = '../ChineseNER/other/train.log'
    map_file = '../ChineseNER/other/maps.pkl'
    ckpt_path = '../ChineseNER/other/ckpt'
    other_result = evaluate_entities_core(line, config_file, log_file, map_file, ckpt_path)

    other_entities = list(set([f['word'] for f in other_result['entities']]))

    result = ' '.join(food_entities + other_entities)
    return result


def evaluate_entities_core(line, config_file='../ChineseNER/config_file', log_file='../ChineseNER/train.log',
                           map_file='../ChineseNER/maps.pkl', ckpt_path='../ChineseNER/ckpt'):
    """ 调用模型得到命名实体

    Args:
        line: 预处理后的文档文本
        config_file: 配置文件路径
        log_file: 日志文件路径
        map_file: 映射文件路径
        ckpt_path: 模型文件路径

    Returns: 字典，字典里的entities命名实体是list，list中每个元素是字典。字典格式为：
             result:
                 {
                 'string':'xxxxxxx',
                 'entities':[{x},{y}]
                 }
             x:
                 {
                 'word':'三无产品',
                 'start':10,
                 'end':14,
                 'type':'Food'
                 }
    """
    config = ChineseNER.utils.load_config(config_file)
    logger = ChineseNER.utils.get_logger(log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(map_file, "rb") as f:
        char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        model = ChineseNER.utils.create_model(sess, Model, ckpt_path,
                                              ChineseNER.data_utils.load_word2vec, config, id_to_char, logger)
        result = model.evaluate_line(sess, ChineseNER.data_utils.input_from_line(line, char_to_id), id_to_tag)
        print(result)
        return result


def test_doc_sim(doc1, doc2):
    i = 0
    model_path = os.path.join(model_dir, "doc2vec" + str(i) + ".model")
    model = gensim.models.Doc2Vec.load(model_path)
    doc1 = doc1.split()
    doc2 = doc2.split()
    vec1_1 = model.infer_vector(doc1)
    vec2_1 = model.infer_vector(doc2)
    vec1_2 = sent2vec(model, doc1)
    vec2_2 = sent2vec(model, doc2)
    sim1 = test_get_sim(vec1_1, vec2_1)
    print(sim1)
    sim2 = test_get_sim(vec1_2, vec2_2)
    print(sim2)


def test_get_sim(a_vect, b_vect):
    dot_val = 0.0
    a_norm = 0.0
    b_norm = 0.0
    cos = None
    for a, b in zip(a_vect, b_vect):
        dot_val += a * b
        a_norm += a ** 2
        b_norm += b ** 2
    if a_norm == 0.0 or b_norm == 0.0:
        cos = -1
    else:
        cos = dot_val / ((a_norm * b_norm) ** 0.5)
    return cos


def get_cluster_result(topic_num):
    """获得层次聚类后的结果

    Args:
        topic_num: 主题的数量
    """
    print('————开始存储结果————')
    cluster_result_dir = os.path.join('cluster', 'result')
    is_exists = os.path.exists(cluster_result_dir)
    if not is_exists:
        os.makedirs(cluster_result_dir)
    for i in range(topic_num):
        print('————处理第%d个主题————' % i)
        # 存结果矩阵
        cluster_file = os.path.join(cluster_matrix_dir, 'topic' + str(i) + '.matrix')
        matrix = joblib.load(cluster_file)
        pd_matrix = pd.DataFrame(matrix, columns=['doc_index1', 'doc_index2',
                                                  'distance', 'merge_step'])
        result_matrix_file = os.path.join(cluster_result_dir, 'topic' + str(i) + '_matrix.csv')
        pd_matrix.to_csv(result_matrix_file, index=False)

        # 存文档索引
        doc_id_file = os.path.join(vec_dir, 'topic' + str(i) + '_doc.index')
        doc_index = joblib.load(doc_id_file)
        pd_index = pd.DataFrame(doc_index)
        result_index_file = os.path.join(cluster_result_dir, 'topic' + str(i) + '_index.csv')
        pd_index.to_csv(result_index_file, index=True)

    print('————结束存储结果————')


def events_detect():
    print("———————————开始提取事件—————————————")

    print("———开始整理主题文档———")
    # topic_num = get_topic_doc()
    topic_num = 1
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
    # topic_num = 1
    # get_cluster_result(topic_num)
