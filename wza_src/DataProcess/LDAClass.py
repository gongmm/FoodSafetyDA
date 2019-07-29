# -*- coding: utf-8 -*-
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib
import numpy as np
import lda
import sys
import matplotlib.pyplot as plt


class LDAClass:

    def __init__(self, n_topic=36, corpus_file='corpus/news_content_corpus.txt',
                 lda_model_file='model/lda.model',
                 feature_names_model_file='model/feature.model'):
        self.corpus = []
        self.corpus_file = corpus_file
        self.lda_model_file = lda_model_file
        self.feature_names_model_file = feature_names_model_file
        self.n_topic = n_topic

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
        if lda_model is None:
            return
        # 主题-词分布
        topic_word = lda_model.topic_word_
        word = joblib.load(self.feature_names_model_file)
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(word)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
            print(u'*Topic {}\n- {}'.format(i, ' '.join(topic_words)))

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

    def draw_topic_word(self):
        lda_model = joblib.load(self.lda_model_file)
        if lda_model is None:
            return
        # 主题-词分布
        topic_word = lda_model.topic_word_
        f, ax = plt.subplots(5, 1, figsize=(8, 6))
        for i, k in enumerate([1, 5, 9, 14, 19]):
            ax[i].stem(topic_word[k, :], linefmt='b-',
                       markerfmt='bo', basefmt='w-')
            ax[i].set_xlim(-50, 4350)
            ax[i].set_ylim(0, 0.08)
            ax[i].set_ylabel("Prob")
            ax[i].set_title("topic {}".format(k))

        ax[4].set_xlabel("word")

        plt.tight_layout()
        plt.show()

    def draw_doc_topic(self):
        lda_model = joblib.load(self.lda_model_file)
        if lda_model is None:
            return
        # 文档-主题分布 doc_topic
        doc_topic = lda_model.doc_topic_
        f, ax = plt.subplots(5, 1, figsize=(8, 6))
        for i, k in enumerate([1, 3, 4, 8, 9]):
            ax[i].stem(doc_topic[k, :], linefmt='r-',
                       markerfmt='ro', basefmt='w-')
            ax[i].set_xlim(0, self.n_topic)
            ax[i].set_ylim(0, 1)
            ax[i].set_ylabel("Prob")
            ax[i].set_title("Document {}".format(k))

        ax[4].set_xlabel("Topic")

        plt.tight_layout()
        plt.show()

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
        lda_class.train()

    # 获得话题的对应特征词
    # lda_class.save_topic_word()
    lda_class.print_top_words()
    # 在新闻文档中添加话题标签
    lda_class.save_topic('result/doc_topic.csv')
    lda_class.draw_doc_topic()
    # lda_class.draw_topic_word()
    # lda_class.write_doc_topic_to_origin('all_news_data_utf.csv', 'result/all_news_data_utf_topic.csv')
