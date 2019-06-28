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
    corpus = []

    '''读取txt文件里面的内容保存为语料'''

    @staticmethod
    def get_corpus(self, filepath):
        with open(filepath, 'r', encoding='UTF-8') as file:
            for line in file.readlines():
                self.corpus.append(line.strip())
        # print(self.corpus)

    '''打印lda主题词'''

    @staticmethod
    def print_top_words(model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic #%d:" % topic_idx)
            print(" ".join([feature_names[i]
                            for i in topic.argsort()[:-n_top_words - 1:-1]]))
        print()

    '''lda+kmeans'''

    def lda_kmeans(self):
        # 将文本转为词频矩阵
        # 创建词袋数据结构
        cnt_vector = CountVectorizer(max_features=1000)
        # 得到元素--词频
        cnt_tf = cnt_vector.fit_transform(self.corpus)
        # 所有的特征词，即关键词
        cnt_feature = cnt_vector.get_feature_names()
        transformer = TfidfTransformer()
        tf_idf = transformer.fit_transform(cnt_vector.fit_transform(self.corpus))
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
        n_top_words = 20  # 设置主题关键词数
        self.print_top_words(lda, cnt_feature, n_top_words)  # 打印主题词
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

    @staticmethod
    def save_topic(readfile, writefile):
        lda_model = joblib.load('result/model.lda')
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
                        topic_most_pr = 'topicid'
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
                with open('../doc_topic/doctopic.csv', 'w', encoding='utf-8', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(['docid', 'topicid'])
                    for n in range(doc_topic.shape[0]):
                        docid = n
                        topicid = doc_topic[n].argmax()
                        writer.writerow([str(docid), str(topicid)])

    '''将topic存入单独的csv文件'''

    @staticmethod
    def get_topic_word(top_n):
        lda_model = joblib.load('result/model.lda')
        # 主题-词分布
        topic_word = lda_model.topic_word_
        word = joblib.load('result/model.word')
        with open('result/food_topic.csv', 'w', encoding='utf-8', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['topicid', 'topic'])
            for i, topic_dist in enumerate(topic_word):
                topic_words = np.array(word)[np.argsort(topic_dist)][:-(top_n + 1):-1]
                csv_writer.writerow([i, ' '.join(topic_words)])
                print(u'*Topic {}\n- {}'.format(i, ' '.join(topic_words)))

    """lda train"""

    def train(self):
        # 读取文件，生成语料
        print("======生成语料=====")
        self.get_corpus(self, 'corpus/food_news_corpus.txt')

        print("======向量转化=====")
        vectorizer = CountVectorizer()
        x = vectorizer.fit_transform(self.corpus)

        # 获取词袋模型中所有特征词，关键词
        word = vectorizer.get_feature_names()
        joblib.dump(word, 'result/model.word')
        # 词频矩阵，行为文档中的行，列为各个特征词
        weight = x.toarray()
        print("======开始lda=====")

        '''LDA模型调用'''
        lda_model = lda.LDA(n_topics=106, n_iter=1000, random_state=1)
        lda_model.fit(weight)
        joblib.dump(lda_model, 'result/model.lda')


if __name__ == '__main__':
    lda_class = LDAClass()
    # 训练LDA模型
    lda_class.train()
    # 获得话题的对应特征词
    lda_class.get_topic_word(20)
    # 在新闻文档中添加话题标签
    # lda_class.save_topic('data/foodInfo.csv', 'data/foodInfo_topic.csv')
