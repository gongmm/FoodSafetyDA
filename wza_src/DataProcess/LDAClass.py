# -*- coding: utf-8 -*-
import csv
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.externals import joblib
from sklearn import metrics
import numpy as np
import lda


class LDAClass:

    def __init__(self, top_n=20, corpus_file='corpus/news_content_corpus.txt',
                 lda_model_file='model/lda.model', feature_names_model_file='model/feature.model'):
        self.corpus = []
        self.corpus_file = corpus_file
        self.model = None
        self.lda_model_file = lda_model_file
        self.feature_names_model_file = feature_names_model_file
        self.feature_names = None
        self.n_top_words = top_n

    def get_corpus(self):
        """ 读取txt文件里面的内容建立语料库"""
        with open(self.corpus_file, 'r', encoding='UTF-8') as file:
            for line in file.readlines()[:10001]:
                self.corpus.append(line.strip())
        # print(self.corpus)

    '''打印lda主题词'''

    def print_top_words(self):
        for topic_idx, topic in enumerate(self.model.components_):
            print("Topic #%d:" % topic_idx)
            print(" ".join([self.feature_names[i]
                            for i in topic.argsort()[:-self.n_top_words - 1:-1]]))
        print()

    '''lda+kmeans'''

    def lda_kmeans(self):
        # 将文本转为词频矩阵
        # 创建词袋数据结构
        cnt_vector = CountVectorizer(max_features=1000)
        # 得到元素--词频
        cnt_tf = cnt_vector.fit_transform(self.corpus)
        # 所有的特征词，即关键词
        self.cnt_feature = cnt_vector.get_feature_names()
        transformer = TfidfTransformer()
        tf_idf = transformer.fit_transform(cnt_vector.fit_transform(self.corpus))
        tf_idfweight = tf_idf.toarray()
        t0 = time()
        # lda主题聚类
        lda = LatentDirichletAllocation(
            learning_offset=50.,
            random_state=0, max_iter=1000)
        self.model = lda.fit(cnt_tf)
        perplexity = lda.perplexity(X=cnt_tf, sub_sampling=False)
        # 查看lda困惑度
        print(perplexity)
        # 求出文档-主题分布
        doc_res = lda.fit_transform(cnt_tf)
        self.n_top_words = 20  # 设置主题关键词数
        self.print_top_words()  # 打印主题词
        '''聚类，设置K的个数以及质心'''
        kmeans_model = KMeans(n_clusters=111, init='k-means++')
        y_pred = kmeans_model.fit_predict(doc_res)
        print(y_pred)

        labels = kmeans_model.labels_
        # 求其轮廓系数，轮廓系数越大 聚类效果越好
        silhouette = metrics.silhouette_score(doc_res, labels, metric='euclidean')
        print(silhouette)
        print("done in %0.3fs." % (time() - t0))  # 运行的时间

    ''' 将每篇doc对应的topic存储'''

    def save_topic(self, readfile, writefile):
        lda_model = joblib.load(self.lda_model_file)
        # 文档-主题分布 doc_topic
        doc_topic = lda_model.doc_topic_

        print("type(doc_topic):{}".format(type(doc_topic)))
        print("shape:{}".format(doc_topic.shape))
        with open(readfile, 'r', encoding='utf-8') as f_read:
            rows = csv.reader(f_read)
            with open(writefile, 'w', encoding='utf-8', newline='') as f_write:
                writer = csv.writer(f_write)
                n = 0
                for row in rows:
                    if n == 0:
                        topic_most_pr = 'topic_id'
                        row.append(topic_most_pr)
                        # 添加行
                        writer.writerow(row)
                    else:
                        # 选择最可能的主题，对文档进行标记
                        topic_most_pr = doc_topic[n - 1].argmax()
                        row.append(topic_most_pr)
                        writer.writerow(row)
                    n = n + 1

                # doc_topic文档主题分布存入csv文件中
                with open('result/doc_topic.csv', 'w', encoding='utf-8', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['doc_id', 'topic_id'])
                    for n in range(doc_topic.shape[0]):
                        doc_id = n + 1
                        topic_id = doc_topic[n].argmax()
                        writer.writerow([str(doc_id), str(topic_id)])

    '''将topic存入单独的csv文件'''

    def get_topic_word(self):
        lda_model = joblib.load(self.lda_model_file)
        if lda_model is None:
            return
        # 主题-词分布
        topic_word = lda_model.topic_word_
        word = joblib.load(self.feature_names_model_file)
        with open('result/food_topic_word.csv', 'w', encoding='utf-8', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['topic_id', 'topic_word'])
            for i, topic_dist in enumerate(topic_word):
                topic_words = np.array(word)[np.argsort(topic_dist)][:-(self.n_top_words + 1):-1]
                csv_writer.writerow([i, ' '.join(topic_words)])
                print(u'*Topic {}\n- {}'.format(i, ' '.join(topic_words)))

    """lda train"""

    def train(self):
        # 读取文件，生成语料
        print("======生成语料=====")
        self.get_corpus()

        print("======向量转化=====")
        vectorizer = CountVectorizer()
        x = vectorizer.fit_transform(self.corpus)

        # 获取词袋模型中所有特征词，关键词
        word = vectorizer.get_feature_names()
        joblib.dump(word, self.feature_names_model_file)
        # 词频矩阵，行为文档中的行，列为各个特征词
        weight = x.toarray()
        # weight = np.array(x)
        print("======开始lda=====")

        '''LDA模型调用'''
        lda_model = lda.LDA(n_topics=106, n_iter=1000, random_state=1)
        lda_model.fit(weight)
        joblib.dump(lda_model, self.lda_model_file)


if __name__ == '__main__':
    # lda_class = LDAClass(corpus_file='corpus/food_news_corpus.txt')
    lda_class = LDAClass()
    # 训练LDA模型
    lda_class.train()
    # 获得话题的对应特征词
    lda_class.get_topic_word()
    # 在新闻文档中添加话题标签
    lda_class.save_topic('all_news_data_utf.csv', 'all_news_data_utf_topic.csv')
