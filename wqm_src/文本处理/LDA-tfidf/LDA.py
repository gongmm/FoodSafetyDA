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
    data_tag = csv_data['tags']
    data_category = csv_data['category']

    titles,times,links,areas,contents,tags,categorys = [],[],[],[],[],[],[]
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
                tags.append(data_tag[i])
                categorys.append(data_category[i])

        except: #跳过内容为字符串的不符合时间格式要求的
            continue
    #print(corpus)
    print(len(corpus))

    if not os.path.exists('corpus/'+dirname):
        os.mkdir('corpus/'+dirname)

    with open('corpus/'+dirname+'/corpus.json','w') as f: #把语料库（数组格式）保存为json文件，方便下一次直接使用
        json.dump(corpus,f)

    if not os.path.exists('result/'+dirname):
        os.mkdir('result/'+dirname)
    #将符合时间条件的新闻信息保存为新的csv
    dataframe = pd.DataFrame({'time':times,'link':links,'area':areas,'content':contents,'title':titles,'tag':tags,'category':categorys})
    columns = ['title','time','area','tag','category','link','content']  #指定列的顺序
    dataframe.to_csv('result/'+dirname+'/news.csv',index=False,sep=',',columns=columns)
    return corpus

def cluster(filename,begin_time,end_time,dirname):
    """
    LDA主题模型，其中生成doc_topic对应文件，可视化聚类结果
    :param filename:原始文件路径
    :param begin_time:
    :param end_time:
    :param topic_num:聚类指定话题数目
    :param dirname:指定创建新目录名称
    :return:
    """
    topic_num = 10  #聚类主题数目
    iter_num = 50   #模型迭代次数


    if not os.path.exists('corpus/'+dirname+'/corpus.json'):   #生成corpus
        print('开始生成语料库')
        corpus = get_corpus(filename,begin_time,end_time,dirname)
    else:
        print('此语料库已存在，直接加载')
    with open('corpus/'+dirname+'/corpus.json', 'r') as f:
        corpus = json.load(f)   #加载语料库

    print('文本向量化')
    # TF-IDF将文本向量化
    vect = TfidfVectorizer()
    X = vect.fit_transform(corpus)

    print('获取模型中的词语')
    # 获取模型中的词语
    feature_names = np.array(vect.get_feature_names())

    print('LDA主题建模')
    # LDA主题建模，超参α，β取默认值
    model = LatentDirichletAllocation(n_topics=topic_num, learning_method='batch', max_iter=iter_num,
                                      random_state=1)
    lda_topics = model.fit_transform(X)

    # 获取每个topic中的词语
    topic_word = model.components_

    # 存储主题中的topN个关键词
    n = 20
    with open('result/' + dirname + '/topic_words.txt', 'w') as f:
        # print('写入topic——words文件')
        text = ''
        for i, topic_dist in enumerate(topic_word):
            topics = (np.array(feature_names)[np.argsort(topic_dist)][:-(n + 1):-1]).tolist()
            content = ''
            for t in topics:
                content = content + ',' + t
            text = text + str(i) + content + '\n'
        f.write(text)

    # 保存每篇文章最有可能所属的topic类别
    topic_list = []
    for i in range(len(corpus)):
        topic_list.append(lda_topics[i].argmax())

    csv_data = pd.read_csv('result/'+dirname+'/news.csv')
    contents = csv_data['content']
    times = csv_data['time']
    titles = csv_data['title']
    links = csv_data['link']
    areas = csv_data['area']
    tags = csv_data['tag']
    categorys = csv_data['category']
    dataframe = pd.DataFrame({'time': times, 'link': links, 'area': areas, 'content': contents, 'title': titles,'topic':topic_list,'tag':tags,'category':categorys})
    columns = ['title', 'time', 'area', 'tag','category','link', 'content','topic']  # 指定列的顺序
    dataframe.to_csv('result/'+dirname+'/news.csv', index=False, sep=',', columns=columns)

    #可视化聚类结果
    # data = pyLDAvis.sklearn.prepare(model, X, vect)
    # pyLDAvis.save_html(data, 'result/'+dirname+'/LDA.html')
    # pyLDAvis.show(data)

def kmeans_cluster(filename,begin_time,end_time,dirname):
    if not os.path.exists('corpus/'+dirname+'/corpus.json'):   #生成corpus
        print('开始生成语料库')
        corpus = get_corpus(filename,begin_time,end_time,dirname)
    else:
        print('此语料库已存在，直接加载')
    with open('corpus/'+dirname+'/corpus.json', 'r') as f:
        corpus = json.load(f)   #加载语料库

    print('文本向量化')
    # TF-IDF将文本向量化
    vect = TfidfVectorizer()
    X = vect.fit_transform(corpus)

    clf = KMeans(n_clusters = 10)    #自定义聚类的簇
    clf.fit(X)
    #print('7个中心点')
    print(clf.cluster_centers_)
    print('每个样本所属的簇')
    # 每个样本所属的簇
    print(clf.labels_)
    i = 1
    while i <= len(clf.labels_):    #每个样本所属的簇
        print (i, clf.labels_[i - 1])
        i = i + 1

    # # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
    # print("inertia: {}".format(kmeans.inertia_))



if __name__ == '__main__':
    cluster('data/shipin.csv','2018-1-1', '2018-2-1','1月')
    #kmeans_cluster('data/shipin.csv','2018-1-1', '2018-2-1','kmeans')

