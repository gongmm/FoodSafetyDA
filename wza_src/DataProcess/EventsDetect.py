import os
import gensim
import csv
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


result_dir = 'result'
model_dir = 'model'
sim_dir = 'similarity'
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
    news_topic_df = pd.read_csv(news_data_topic_csv)
    doc_num = news_topic_df.shape[0]

    for i in range(1, doc_num+1):
        # 判断文档对应的主题文件夹是否存在
        content, title, topic_id = news_topic_df.loc[i, ['content', 'title', 'topic_id']]
        line = title + '\n' + content
        topic_dir = 'topic_doc/topic' + str(topic_id)
        is_exists = os.path.exists(topic_dir)
        # 如果不存在则创建目录
        if not is_exists:
            os.makedirs(topic_dir)

        file_path = 'topic_doc/topic' + str(topic_id) + \
                    '/topic' + str(topic_id) + '_doc' + str(i) + '.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            # 写入文件
            print(line)
            f.write(line + '\n')  # 把这行写进文件

    return topic_num


def train_model(topic_num):
    """ 训练Doc2Vec，并保存模型

    读取每个主题下的所有文档，对于每个主题训练一个Doc2Vec模型。
    变量doc_labels是一个列表，存放对应主题文件夹下所有文档的文件名。

    Args:
        topic_num: 主题的数量

    """
    for i in range(topic_num):
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
        model = gensim.models.Doc2Vec(vector_size=256, window=8, min_count=1,
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


def get_doc_similarity(topic_num):
    """计算主题中每个文档与该主题的相似度

        中其他所有文档的相似度
    Args:
        topic_num: 主题的数量
    """
    topic_num = 20
    for i in range(topic_num):

        print("load model")
        model_path = os.path.join(model_dir, "doc2vec" + str(i) + ".model")
        model = gensim.models.Doc2Vec.load(model_path)

        data_dir = "topic_doc/topic" + str(i)
        doc_labels = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
        print(len(doc_labels))

        other_str = ""

        is_exists = os.path.exists(sim_dir)
        if not is_exists:
            os.makedirs(sim_dir)
        sim_path = os.path.join(sim_dir, 'topic' + str(i) + '.csv')

        with open(sim_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["doc_id", "similarity"])
            for j in range(len(doc_labels)):
                ws = open(data_dir + "/" + doc_labels[j], 'r', encoding='UTF-8').read()  # 一行文件
                list1 = ws.split()

                # 拼接topic下其他所有文档
                for doc in doc_labels:
                    if doc != doc_labels[j]:
                        ws = open(data_dir + "/" + doc, 'r', encoding='UTF-8').read()  # 一行文件
                        other_str = other_str + ws
                list2 = other_str.split()
                print(doc_labels[j])

                # 转成句子向量
                vect1 = sent2vec(model, list1)
                vect2 = sent2vec(model, list2)

                # 查看变量占用空间大小
                import sys
                print(sys.getsizeof(vect1))
                print(sys.getsizeof(vect2))

                # 得到向量间的相似度
                cos = similarity(vect1, vect2)
                print("相似度：{:.4f}".format(cos))

                # 得到doc_id
                doc_id = doc_labels[j].split('doc')[1].split('.')[0]
                writer.writerow([doc_id, cos])


def similarity(a_vect, b_vect):
    """ 计算两个向量的余弦值

    Args:
        a_vect: a 向量
        b_vect: b 向量
    """
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


def sent2vec(model, words):
    """ 文本转换成向量

    Args:
        model: Doc2Vec模型
        words: 分词后的文本

    Returns:
        向量数组
    """
    vect_list = []
    for w in words:
        try:
            vect_list.append(model.wv[w])
        except Exception as e:
            # print(e)
            continue
    vect_list = np.array(vect_list)
    vect = vect_list.sum(axis=0)
    return vect / np.sqrt((vect ** 2).sum())


class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield gensim.models.doc2vec.LabeledSentence(words=doc.split(), tags=[self.labels_list[idx]])


def get_entity_similarity():
    """计算文档中提取的命名实体相似度

    获得文档中提取出食品专有名词及时间、地点、人物等专有名词的相似度。
    """
    pass


def get_total_similarity():
    """获得加权的总相似度

    Sim(d1, d2) = w * Sim_doc(d1, d2) + (1-w) * Sim_entity(d1, d2)
    d1，d2为两个不同的文档；
    w为文档相似度的权重，需要实验得出；
    Sim_doc(d1, d2)计算文档相似度
    Sim_entity(d1, d2)计算文档中提取的命名实体相似度
    """
    w = 0.7  # weight
    sim_doc = 1
    sim_entity = 1
    sim = w * sim_doc + (1 - w) * sim_entity


def events_detect():
    # topic_num = get_topic_doc()

    topic_num = 36

    #train_model(topic_num)

    get_doc_similarity(topic_num)

    # get_entity_similarity()

    # get_total_similarity()

    # 得到的相似度和阈值比较，大于阈值则为新的事件，小于阈值则为同一事件


if __name__ == '__main__':
    events_detect()
