import os
import jieba
import pandas as pd
import datetime
import json
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import pyLDAvis
import pyLDAvis.sklearn
import pyLDAvis.gensim
import lda
import lda.datasets
import csv
import heapq
import imp

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

def get_words(text):
    """
    文本预处理，分词，去停用词
    :param text: 待预处理的文本
    :return: content, 按空格分隔的分词后文本
    """
    stopfile = 'settings/stop_words.txt'
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

def get_corpus(filename,begin_t,end_t,dirname):
    """
    读取csv文件，按照时间获取corpus
    :param filename:原始csv文件
    :param begin_time:
    :param end_time:
    :param dirname:指定创建新目录的名称
    :return:
    """
    begin_time = datetime.datetime.strptime(begin_t, "%Y-%m-%d")
    end_time = datetime.datetime.strptime(end_t, "%Y-%m-%d")
    csv_data = pd.read_csv(filename)
    data_content = csv_data['content']
    data_time = csv_data['time']
    data_title = csv_data['title']
    data_link = csv_data['link']
    data_area = csv_data['area']

    titles,times,links,areas,contents = [],[],[],[],[]
    corpus = [] #语料库
    for i in range(len(data_time)):
        if type(data_time[i])==float:   #跳过内容为nan的
            continue
        try:
            time = datetime.datetime.strptime(data_time[i], "%Y/%m/%d %H:%M")
            if time>begin_time and time<end_time:   #符合时间要求的
                words = get_words(data_content[i])
                corpus.append(words)
                titles.append(data_title[i])
                times.append(data_time[i])
                links.append(data_link[i])
                areas.append(data_area[i])
                contents.append(data_content[i])

        except: #跳过内容为字符串的不符合时间格式要求的
            continue
    #print(corpus)
    print(len(corpus))
    with open('corpus/'+str(begin_t)+'.json','w') as f: #把语料库（数组格式）保存为json文件，方便下一次直接使用
        json.dump(corpus,f)

    #将符合时间条件的新闻信息保存为新的csv
    dataframe = pd.DataFrame({'time':times,'link':links,'area':areas,'content':contents,'title':titles})
    columns = ['title','time','area','link','content']  #指定列的顺序
    dataframe.to_csv('result/'+str(begin_t)+'.csv',index=False,sep=',',columns=columns)
    return corpus

def cluster(filename,begin_time,end_time,dirname):
    """
    LDA主题模型聚类，其中生成doc_topic对应文件，可视化聚类结果
    :param filename:原始文件路径
    :param begin_time:
    :param end_time:
    :param topic_num:聚类指定话题数目
    :param dirname:指定创建新目录名称
    :return:
    """
    topic_num = 10  #聚类主题数目
    iter_num = 50   #模型迭代次数


    if not os.path.exists('corpus/'+str(begin_time)+'.json'):   #生成corpus
        print('开始生成语料库')
        corpus = get_corpus(filename,begin_time,end_time)
    else:
        print('此语料库已存在，直接加载')
    with open('corpus/'+str(begin_time)+'.json', 'r') as f:
        corpus = json.load(f)   #加载语料库

    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()

    # fit_transform是将文本转为词频矩阵
    tf = vectorizer.fit_transform(corpus)

    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()
    analyze = vectorizer.build_analyzer()
    weight = tf.toarray()

    model = lda.LDA(n_topics=topic_num, n_iter=iter_num, random_state=1)  #话题数目，迭代次数
    model.fit(np.asarray(weight))  # model.fit_transform(tf) is also available
    topic_word = model.topic_word_  # model.components_ also works


    # 存储主题中的TopN关键词
    n = 15
    with open('result/topic_words'+str(begin_time)+'.txt','w') as f:
        text = ''
        for i, topic_dist in enumerate(topic_word):

            topics = (np.array(word)[np.argsort(topic_dist)][:-(n + 1):-1]).tolist()
            content= ''
            for t in topics:
                content = content+','+t
            text = text+str(i)+content+'\n'
        f.write(text)

    # 文档-主题（Document-Topic）分布
    doc_topic = model.doc_topic_
    print("shape: {}".format(doc_topic.shape))

    # 保存每篇文章对应的最大可能的topic序号
    topic_list = []
    for i in range(len(corpus)):
        topic_list.append(doc_topic[n].argmax())

    csv_data = pd.read_csv('result/'+str(begin_time)+'.csv')
    contents = csv_data['content']
    times = csv_data['time']
    titles = csv_data['title']
    links = csv_data['link']
    areas = csv_data['area']
    dataframe = pd.DataFrame({'time': times, 'link': links, 'area': areas, 'content': contents, 'title': titles,'topic':topic_list})
    columns = ['title', 'time', 'area', 'link', 'content','topic']  # 指定列的顺序
    dataframe.to_csv('result/' + str(begin_time) + '.csv', index=False, sep=',', columns=columns)

    #可视化聚类结果
    data = pyLDAvis.sklearn.prepare(model, tf, vectorizer)
    pyLDAvis.save_html(data, 'result/LDA_topic'+str(begin_time)+'.html')
    pyLDAvis.show(data)




if __name__ == '__main__':
    cluster('data/shipin.csv','2018-1-1', '2018-12-31')
