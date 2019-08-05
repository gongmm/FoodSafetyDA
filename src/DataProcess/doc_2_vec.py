import os

import jieba
import gensim
import numpy as np
from sklearn.externals import joblib

from event_util import sort_key

model_dir = 'model'
vec_dir = 'vec_arr'


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
    for i in range(10, topic_num):
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