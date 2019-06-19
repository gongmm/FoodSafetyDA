import os
import jieba
import pandas as pd
import datetime
import json
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn
import pyLDAvis.gensim
import lda
import lda.datasets
import csv
import heapq
import imp
from sklearn.cluster import KMeans
import jieba.analyse
from collections import Counter

import matplotlib.pyplot as plt
import itertools

from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import svm,datasets

from sklearn.externals import joblib


#在运行时需要先删除文件夹中mac系统自带的.DS_store文件
#find ./ -name ".DS_Store" -depth -exec rm {} \;

def clean_csv(filename):
    """
    清洗csv文件
    :param filename:
    :return:
    """
    data = pd.read_csv(filename)
    data_title = data['title']
    data_pubdate = data['pubdate']
    data_url = data['url']
    data_content = data['content']

    title,pubdate,url,content = [],[],[],[]
    for i in range(len(data)):
        if type(data_content[i])==float:
            continue
        else:
            title.append(data_title[i])
            pubdate.append(data_pubdate[i])
            url.append(data_url[i])
            content.append(data_content[i])
    dateFrame = pd.DataFrame({'title':title,'pubdate':pubdate,'url':url,'content':content},columns=['title','pubdate','url','content'])
    dateFrame.to_csv('food_new.csv',index=True,sep=',')

def fenci(text):
    """
    文本分词
    :param text: 原始文本
    :return: word
    """
    uncn = re.compile(r'[\u4e00-\u9fa5]')   #正则表达式分离出文本中的中文
    en = "".join(uncn.findall(text.lower()))    #分离的中文文本
    words = jieba.lcut(en)   #结巴分词
    return words

def preprocess(text):
    """
    文本预处理，分词，去停用词
    :param text: 待预处理的文本
    :return: content, 按空格分隔的分词后文本
    """
    stopfile = '文本处理/文本分类/settings/stop_words.txt'
    with open (stopfile,'r',encoding='utf-8') as f:
        stop_content = f.read()
    stop_list = stop_content.splitlines()   #停用词列表
    words = fenci(text) #分词后
    content = ' '
    for word in words:
        if word in stop_list:
            continue
        content = content+' '+word
    #print(content)
    return content


def text_keyword(text,topK):
    """
    提取文本关键词
    :param text: 原始文本
    :param topK: 关键词个数
    :return:
    """
    jieba.analyse.set_stop_words("文本处理/文本分类/settings/stop_words.txt")  # 加载自定义停用词表
    keywords = jieba.analyse.textrank(text, topK=topK, allowPOS=('n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd'))  # TextRank关键词提取，词性筛选
    word_split = " ".join(keywords)
    #print(word_split)
    return word_split


def make_Dictionary(filename):
    """
    构建主题话题词典
    :param trainfile:
    :return:
    """
    corpus = [] #词组

    for path in file_name(filename):
        #print(path)
        with open(filename+path,'r',encoding='utf-8') as f:
            text = f.read()
        clean_text = text_keyword(text,20)
        for word in clean_text.split():
            corpus.append(word)

    # Counter是一个无序的容器类型，以字典的键值对形式存储，其中元素作为key，其计数作为value
    dictionary = Counter(corpus)
    list_count = dictionary.keys()
    #print(list_count)
    dictionary = dictionary.most_common(30)
    #print('_______')
    #print(dictionary)
    return dictionary


def file_name(file_dir):
    """
    获取文件夹下文件
    :param file_dir:
    :return:
    """
    for root, dirs, files in os.walk(file_dir):
        return files


def extract_features(filename):
    """
    特征权重计算和文本表示
    :param filename:
    :return:
    """
    corpus_food = make_Dictionary('文本处理/文本分类/data/food/') #生成主题词典
    docID = 0  # 定义文档编号
    features_matrix = np.zeros((len(file_name(filename)), 30))  # 通过numpy创建维度为30，数量为文件个数，值为0的矩阵


    # 读取目标文件夹下所有子文件(txt类型)
    for path in file_name(filename):
        # 打开并读取文件
        with open(filename + path, "r", encoding='utf-8') as f:
            content = f.read()

        x_ = text_keyword(content,30)   #提取前30个关键词

        # 遍历抽取到的关键词
        for word in x_.split():
            wordID = 0
            # 遍历做好的字典，关键词在哪个位置上出现，便对此位置赋值，值的大小可以取字典元素的值，也可以再增加倍数
            for i, d in enumerate(corpus_food):
                #若该词等于主题词典中的词
                if d[0] == word:
                    wordID = i
                    features_matrix[docID, wordID] = x_.split().count(word) * d[1]

        # 将单个文本的向量转化为DataFrame对象，DataFrame是一种二维表
        corpus = pd.DataFrame(features_matrix)
        # 文档编号加1
        docID += 1
    # 将文本转化的矩阵和文件名称对应起来，方便检查
    corpus['name'] = file_name(filename)
    #print(corpus)
    return corpus

def train_NB():
    """
    训练高斯贝叶斯模型
    :return:
    """
    print('得到junk向量模型')
    df_junk = extract_features('文本处理/文本分类/data/new_junk/')
    df_junk['kind'] = 0
    print('得到food向量模型')
    df_food = extract_features('文本处理/文本分类/data/new_food/')
    df_food['kind'] = 1
    df = df_food.append(df_junk)
    df = df.reset_index(drop=True)  #总的数据集

    # 使用train_test_split工具随机分配训练集，测试集,随机拿出百分之30的数据做测试
    # train_data：样本特征集  train_target：样本标签  test_size：测试样本占比
    # 返回训练集测试集样本，训练集测试集标签
    # X_train,X_test, y_train, y_test =cross_validation.train_test_split(train_data,train_target,test_size=0.3, random_state=0)
    X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, :30], df.iloc[:, 31], test_size=0.20)


    print('创建高斯贝叶斯模型')
    # 创建高斯贝叶斯模型
    model = GaussianNB()
    model.fit(X_train, y_train)

    # 测试集的预测结果
    result = model.predict(X_test)

    # 构建混淆矩阵
    confusion = confusion_matrix(y_test, result)

    print('画图')
    plt.imshow(confusion, interpolation='nearest', cmap=plt.cm.Oranges)
    plt.xlabel('Predict_Label')
    plt.ylabel('True_Label')
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, rotation=90)
    plt.yticks(tick_marks)
    plt.colorbar()

    plt.title('NB_confustion_matrix')
    for i, j in itertools.product(range(len(confusion)), range(len(confusion))):
        plt.text(i, j, confusion[j, i],
                 horizontalalignment="center")
    plt.show()
    print('画图完成')
    joblib.dump(model, "文本处理/文本分类/data/train_model_NB.m")

def train_SVM():
    """
    训练SVM模型
    :return:
    """
    df_junk = extract_features('文本处理/文本分类/data/new_junk/')
    df_junk['kind'] = 0
    df_food = extract_features('文本处理/文本分类/data/new_food/')
    df_food['kind'] = 1
    df = df_food.append(df_junk)
    df = df.reset_index(drop=True)
    X_train, X_test, y_train, y_test = train_test_split(df.iloc[:, :30], df.iloc[:, 31], test_size=0.20)

    # 创建svm模型
    print(' 创建svm模型')
    model = svm.SVC(kernel="rbf", C=1)
    model.fit(X_train, y_train)
    result = model.predict(X_test)
    confusion = confusion_matrix(y_test, result)

    print('画图')
    plt.imshow(confusion, interpolation='nearest', cmap=plt.cm.Oranges)
    plt.xlabel('Predict_Label')
    plt.ylabel('True_Label')
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, rotation=90)
    plt.yticks(tick_marks)
    plt.colorbar()

    plt.title('SVM_confustion_matrix')
    for i, j in itertools.product(range(len(confusion)), range(len(confusion))):
        plt.text(i, j, confusion[j, i],
                 horizontalalignment="center")
    plt.show()
    print('画图完成')
    joblib.dump(model, "文本处理/文本分类/data/train_model_SVM.m")

def predict_text(modelname,result_name):
    """
    利用模型预测数据
    :return:
    """
    clf = joblib.load(modelname)
    df_pre = extract_features('文本处理/文本分类/data/new_predict/')

    pre_result = clf.predict(df_pre.iloc[:, :30])
    df_pre['tag'] = pre_result

    # 将预测结果存入csv文件
    df_pre.to_csv(result_name,index=False,sep=',')

def show_result(filename):
    """
    展示结果
    :param filename:
    :return:
    """
    print('***************************')
    print('属于食品安全话题的有以下：')
    csv_data = pd.read_csv(filename)
    names = csv_data['name']
    tags = csv_data['tag']
    food = 0
    for i in range(len(csv_data)):
        if tags[i]==1:
            food +=1
            print(names[i])
    print('***************************')
    print('与话题相关的:'+str(food)+'  与话题无关的:'+str(len(csv_data)-food))

if __name__ == '__main__':
    #train_NB() #训练模型
    #train_SVM()

    # print('______用朴素贝叶斯模型来预测______')
    # predict_text('文本处理/文本分类/data/train_model_NB.m','文本处理/文本分类/result/predict_NB.csv')
    # show_result('文本处理/文本分类/result/predict_NB.csv')

    print('______用SVM模型来预测______')
    predict_text('文本处理/文本分类/data/train_model_SVM.m','文本处理/文本分类/result/predict_SVM.csv')
    show_result('文本处理/文本分类/result/predict_SVM.csv')






