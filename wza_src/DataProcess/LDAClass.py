# -*- coding: utf-8 -*-
import csv
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from time import time
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.externals import joblib
from sklearn import metrics
import numpy as np
import lda
import sys


class LDAClass:

    def __init__(self, n_topic=36, corpus_file='corpus/news_content_corpus.txt',
                 lda_model_file='model/lda.model',
                 feature_names_model_file='model/feature.model',
                 doc_topic_dist_file='model/sk_doc_topic.model'):
        self.corpus = []
        self.corpus_file = corpus_file
        self.lda_model_file = lda_model_file
        self.feature_names_model_file = feature_names_model_file
        self.n_topic = n_topic
        self.sk_doc_topic_file = doc_topic_dist_file

    def get_corpus(self):
        """ 读取txt文件里面的内容建立语料库"""
        with open(self.corpus_file, 'r', encoding='UTF-8') as file:
            # for line in file.readlines()[:10000]:
            for line in file.readlines():
                self.corpus.append(line.strip())
        print(len(self.corpus))
        # print(self.corpus)

    def print_top_words(self, n_top_words=20):
        """ 打印lda主题词

        Args:
            n_top_words : 选取的关键词个数
        """
        lda_model = joblib.load(self.lda_model_file)
        doc_topic_dist = joblib.load(self.sk_doc_topic_file)
        tf_feature_names = joblib.load(self.feature_names_model_file)

        if lda_model is None:
            return
        # 主题-词分布
        # topic_word = lda_model.topic_word_
        for topic_idx, topic in enumerate(lda_model.components_):
            print("Topic #%d:" % topic_idx)
            print(" ".join([tf_feature_names[i]
                            for i in topic.argsort()[:-n_top_words - 1:-1]]))

        print("type(doc_topic):{}".format(type(doc_topic_dist)))
        print("shape:{}".format(doc_topic_dist.shape))
        with open('all_news_data_utf.csv', 'r', encoding='utf-8') as f_read:
            rows = csv.reader(f_read)
            with open('result/all_news_data_utf_topic_sk.csv', 'w', encoding='utf-8', newline='') as f_write:
                writer = csv.writer(f_write)
                n = 0
                for row in rows:
                    if n == 0:
                        topic_most_pr = 'topic_id'
                        row.append(topic_most_pr)
                        # 添加行
                        writer.writerow(row)
                    # elif n <= 10000:
                    else:
                        # 选择最可能的主题，对文档进行标记
                        topic_most_pr = doc_topic_dist[n - 1].argmax()
                        row.append(topic_most_pr)
                        writer.writerow(row)
                    n = n + 1

    def lda_kmeans(self):
        """lda+kmeans"""
        # 将文本转为词频矩阵
        # 创建词袋数据结构
        cnt_vector = CountVectorizer(max_features=1000)
        # 得到元素--词频
        cnt_tf = cnt_vector.fit_transform(self.corpus)
        # 所有的特征词，即关键词

        self.cnt_feature = cnt_vector.get_feature_names()
        transformer = TfidfTransformer()
        tf_idf = transformer.fit_transform(cnt_tf)
        tf_idfweight = tf_idf.toarray()
        t0 = time()
        # lda主题聚类
        lda = LatentDirichletAllocation(
            learning_offset=50.,
            random_state=0, max_iter=1000)
        lda.fit(cnt_tf)
        perplexity = lda.perplexity(X=cnt_tf, sub_sampling=False)
        # 查看lda困惑度
        print(perplexity)
        # 求出文档-主题分布
        doc_res = lda.fit_transform(cnt_tf)
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

    def save_topic(self, writefile):
        """ 将每篇doc对应的topic存储 [doc_id, topic_id]
            doc_id 从1开始
            topic_id 从0开始

        Args:
            writefile: 写入的新文件地址

        Returns:

        """
        lda_model = joblib.load(self.lda_model_file)
        # 文档-主题分布 doc_topic
        doc_topic = lda_model.doc_topic_

        print("type(doc_topic):{}".format(type(doc_topic)))
        print("shape:{}".format(doc_topic.shape))
        # 计算前10篇文档最可能的主题
        for n in range(10):
            topic_most_pr = doc_topic[n].argmax()
            print("doc: {} topic: {}".format(n, topic_most_pr))
        # doc_topic文档主题分布存入csv文件中
        with open(writefile, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['doc_id', 'topic_id'])
            for n in range(doc_topic.shape[0]):
                doc_id = n + 1
                topic_id = doc_topic[n].argmax()
                writer.writerow([str(doc_id), str(topic_id)])

    def write_doc_topic_to_origin(self, readfile, writefile):
        """ 在原文档后加一列表示每篇文档对应的主题

        Args:
            readfile: 读取的源文件的地址
            writefile: 写入的新文件地址

        Returns:

        """
        lda_model = joblib.load(self.lda_model_file)
        # 文档-主题分布 doc_topic
        doc_topic = lda_model.doc_topic_
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
                    # elif n <= 10000:
                    else:
                        # 选择最可能的主题，对文档进行标记
                        topic_most_pr = doc_topic[n - 1].argmax()
                        row.append(topic_most_pr)
                        writer.writerow(row)
                    n = n + 1

    def save_topic_word(self, n_top_words=20, writefile='result/food_topic_word.csv'):
        """将话题关键词存入单独的csv文件 ['topic_id', 'topic_word']

        Args:
            n_top_words: 选取的关键词个数
            writefile : 写入的文件路径
        """
        lda_model = joblib.load(self.lda_model_file)
        if lda_model is None:
            return
        # 主题-词分布
        topic_word = lda_model.topic_word_
        word = joblib.load(self.feature_names_model_file)
        with open(writefile, 'w', encoding='utf-8', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['topic_id', 'topic_word'])
            for i, topic_dist in enumerate(topic_word):
                topic_words = np.array(word)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
                csv_writer.writerow([i, ' '.join(topic_words)])
                print(u'*Topic {}\n- {}'.format(i, ' '.join(topic_words)))

    def sklearn_lda(self):
        """利用 sklearn 中的 lda 模型进行训练"""
        print("======生成语料=====")
        self.get_corpus()
        print("Extracting tf features for LDA...")
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                        max_features=2000,
                                        stop_words='english')
        t0 = time()
        tf = tf_vectorizer.fit_transform(self.corpus)
        print("done in %0.3fs." % (time() - t0))
        print()
        print("======开始sklean_LDA=====")
        lda = LatentDirichletAllocation(n_components=self.n_topic, max_iter=5,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=0)
        t0 = time()
        lda.fit(tf)
        print("done in %0.3fs." % (time() - t0))

        print("\nTopics in LDA model:")
        tf_feature_names = tf_vectorizer.get_feature_names()
        joblib.dump(tf_feature_names, self.feature_names_model_file)
        for topic_idx, topic in enumerate(lda.components_):
            message = "Topic #%d: " % topic_idx
            message += " ".join([tf_feature_names[i]
                                 for i in topic.argsort()[:-self.n_topic - 1:-1]])
            print(message)
        print()

        t0 = time()
        doc_topic_dist = lda.transform(tf)
        joblib.dump(lda, self.lda_model_file)
        joblib.dump(doc_topic_dist, self.sk_doc_topic_file)
        print("done in %0.3fs." % (time() - t0))
        print("lda perplexity %.3f" % lda.perplexity(tf))

    def train(self):
        """lda train"""
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
        print("======开始lda=====")
        # LDA模型调用
        lda_model = lda.LDA(n_topics=self.n_topic, n_iter=100, random_state=0)
        lda_model.fit(weight)
        joblib.dump(lda_model, self.lda_model_file)


if __name__ == '__main__':
    # lda_class = LDAClass(corpus_file='corpus/food_news_corpus.txt')
    lda_class = LDAClass()
    if len(sys.argv) > 1:
        if sys.argv[-1] == 'sk':
            lda_class = LDAClass(lda_model_file='model/lda_sk.model',
                                 feature_names_model_file='model/feature_sk.model')
            # 训练LDA模型
            # lda_class.sklearn_lda()
        else:
            lda_class.train()

    # 获得话题的对应特征词
    # lda_class.save_topic_word()
    lda_class.print_top_words()
    # 在新闻文档中添加话题标签
    # lda_class.save_topic('result/doc_topic.csv')
    # lda_class.write_doc_topic_to_origin('all_news_data_utf.csv', 'result/all_news_data_utf_topic.csv')
