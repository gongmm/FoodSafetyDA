# -*- coding: utf-8 -*-
import csv
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from  matplotlib import pyplot
from matplotlib import colors
import os
from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
# 遍历指定目录，显示目录下的所有文件名
class ldaclass:
    corpus = []

    '''读取txt文件里面的内容保存为语料'''
    def readtxt(self,filepath):
        with open(filepath,'r', encoding='UTF-8') as f:
            for line in f.readlines():
                self.corpus.append(line.strip())
        print(self.corpus)

    '''打印lda主题词'''
    def print_top_words(self,model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
             print("Topic #%d:" % topic_idx)
             print(" ".join([feature_names[i]
             for i in topic.argsort()[:-n_top_words - 1:-1]]))
        print()
    '''lda+kmeans'''
    def lda_keans(self):
        # 将文本转为词频矩阵
        cntVector = CountVectorizer(max_features=1000)
        cntTf = cntVector.fit_transform(self.corpus)
        cnfeature=cntVector.get_feature_names()#所有的特征词
        transformer=TfidfTransformer()
        tf_idf=transformer.fit_transform(cntVector.fit_transform(self.corpus))
        tf_idfweight=tf_idf.toarray()
        t0=time()
        #lda主题聚类
        lda = LatentDirichletAllocation(n_topics=111,
                                        learning_offset=50.,
                                        random_state=0,max_iter=1000)
        lda.fit(cntTf)
        perplexity=lda.perplexity(X=cntTf,sub_sampling=False)
        print (perplexity)#查看lda困惑度
        docres = lda.fit_transform(cntTf)#求出文档-主题分布
        n_top_words = 20#设置主题关键词数
        self.print_top_words(lda, cnfeature, n_top_words)#打印主题词
        # cm=colors.ListedColormap(list('rgbm'))
        '''聚类，设置K的个数以及质心'''
        kmeans_model=KMeans(n_clusters=111,init='k-means++')
        y_pred=kmeans_model.fit_predict(docres)
        print (y_pred)
        from sklearn import metrics
        labels = kmeans_model.labels_
        #求其轮廓系数，轮廓系数越大 聚类效果越好
        lunkuo=metrics.silhouette_score(docres, labels, metric='euclidean')
        print (lunkuo)
        print("done in %0.3fs." % (time() - t0))#运行的时间
    # pyplot.scatter(docres[:,0],docres[:,1],c=y_pre,cmap=cm)
    # pyplot.title(u"K-means聚类")
    # pyplot.grid()
    # pyplot.show()
    #
    # import pyLDAvis
    # import pyLDAvis.sklearn
    # pyLDAvis.enable_notebook()
    # pyLDAvis.sklearn.prepare(ldatest, tf, tf_vectorizer)
    #绘图
    #降维绘图
    # def plotpic(y_pred):
    #     from sklearn.decomposition import PCA
    #
    #     pca = PCA(n_components=2)  # 输出两维
    #     newData = pca.fit_transform(docres)  # 载入N维
    #     # print newData
    #     x = [n[0] for n in newData]
    #     y = [n[1] for n in newData]
    #
    #     x1, y1 = [], []
    #     x2, y2 = [], []
    #     x3, y3 = [], []
    #     x4, y4 = [], []
    #     x5, y5 = [], []
    #     x6, y6 = [], []
    #
    #     # 分别获取类标为0、1、2的数据 赋值给(x1,y1) (x2,y2) (x3,y3)
    #     i = 0
    #     while i < len(newData):
    #         if y_pred[i] == 0:
    #             x1.append(newData[i][0])
    #             y1.append(newData[i][1])
    #         elif y_pred[i] == 1:
    #             x2.append(newData[i][0])
    #             y2.append(newData[i][1])
    #         elif y_pred[i] == 2:
    #             x3.append(newData[i][0])
    #             y3.append(newData[i][1])
    #         elif y_pred[i] == 3:
    #             x4.append(newData[i][0])
    #             y4.append(newData[i][1])
    #         elif y_pred[i] == 4:
    #             x5.append(newData[i][0])
    #             y5.append(newData[i][1])
    #         elif y_pred[i] == 5:
    #             x5.append(newData[i][0])
    #             y5.append(newData[i][1])
    #         elif y_pred[i] == 6:
    #             x6.append(newData[i][0])
    #             y6.append(newData[i][1])
    #         i = i + 1
    #
    #     import matplotlib.pyplot as plt
    #
    #     # 三种颜色
    #     plot1, = plt.plot(x1, y1, marker="o", markersize=10)
    #     plot2, = plt.plot(x2, y2, marker="o", markersize=10)
    #     plot3, = plt.plot(x3, y3, marker="o", markersize=10)
    #     plot4, = plt.plot(x4, y4, marker="o", markersize=10)
    #     plot5, = plt.plot(x5, y5, marker="o", markersize=10)
    #     plot6, = plt.plot(x6, y6, marker="o", markersize=10)
    #     plt.title("K-Means Text Clustering")  # 绘制标题
    #     plt.legend((plot1, plot2, plot3, plot4, plot5, plot6), ('A', 'B', 'C', 'D', 'E', 'F'))
    #
    #     plt.show()
    def lda_cipintest(self):
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.feature_extraction.text import TfidfTransformer
        print("======向量转化=====")
        vectorizer=CountVectorizer()
        X=vectorizer.fit_transform(self.corpus)
        #transformer=TfidfTransformer()
        #tfidf=transformer.fit_transform(X)
        word=vectorizer.get_feature_names()#获取词袋模型中所有特征词
        weight=X.toarray()#词频矩阵
        #tfidf_weight=tfidf.toarray()#tf-idf矩阵
        print ("======开始lda=====")
       # print (tfidf_weight)
        #打印特征词
        # for j in range(len(word)):
        #     print (word[j],)
        import numpy as np
        import lda
        '''LDA模型调用'''
        ldamodel = lda.LDA(n_topics=106, n_iter=1000, random_state=1)
        ldamodel.predict()
        ldamodel.fit(weight)
        #主题-词分布
        topic_word=ldamodel.topic_word_
        n=20#输出前5个主题词
        '''将topic存入单独的csv文件'''
        with open('../csv/testcsv/shipintopic.csv','w',encoding='utf-8', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['topicid', 'topic'])
            for i, topic_dist in enumerate(topic_word):
                topic_words = np.array(word)[np.argsort(topic_dist)][:-(n + 1):-1]
                list=[]
                list.append(i)
                list.append(' '.join(topic_words))
                csv_writer.writerow(list)
                print(u'*Topic {}\n- {}'.format(i, ' '.join(topic_words)))
        #文档-主题分布 doc_topic
        doc_topic=ldamodel.doc_topic_

        print("type(doc_topic):{}".format(type(doc_topic)))
        print("shape:{}".format(doc_topic.shape))
        ''' 将每篇doc对应的topic存储'''
        with open('../csv/testcsv/shipinprocess.csv', 'r', encoding='utf-8') as f:
            rows = csv.reader(f)
            with open('../csv/testcsv/shipinprocess_new.csv', 'w', encoding='utf-8', newline='') as f1:
                writer = csv.writer(f1)
                n = 0
                for row in rows:
                    if n==0:
                      topic_most_pr='topicid'
                      row.append(topic_most_pr)
                      #添加行
                      writer.writerow(row)
                    else:
                        topic_most_pr = doc_topic[n-1].argmax()
                        row.append(topic_most_pr)
                        writer.writerow(row)
                    n = n + 1
                # with open('./doc_topic.txt', 'w', encoding='utf-8') as f:
                #     for n in range(doc_topic.shape[0]):
                #         topic_most_pr = doc_topic[n].argmax()
                #         print("doc: {} topic: {}".format(n, topic_most_pr))
                #         f.write("doc: " + str(n) + " topic: " + str(topic_most_pr) + "")
                #         f.write('\n')
                #doc_topic文档主题分布存入csv文件中
                with open('../doc_topic/doctopic.csv', 'w', encoding='utf-8', newline='') as csvffile:
                    writer = csv.writer(csvffile)
                    writer.writerow(['docid', 'topicid'])
                    for n in range(doc_topic.shape[0]):
                        docid = n
                        topicid = doc_topic[n].argmax()
                        writer.writerow([str(docid), str(topicid)])

if __name__=='__main__':
    ldaclass=ldaclass()
    #通过test文件夹下所有文件统计为一个文档中
    #读取文件，生成语料
    ldaclass.readtxt('../corpus/doc_shipin.txt')
    ldaclass.lda_cipintest()
    #from numpy import random

    #doc_topic = random.random(size=(10890, 81))

