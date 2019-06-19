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
    data_keyword = csv_data['keyword']

    titles,times,links,areas,contents,tags,categorys,keywords = [],[],[],[],[],[],[],[]
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
                keywords.append(data_keyword[i])

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
    dataframe = pd.DataFrame({'time':times,'link':links,'area':areas,'content':contents,'title':titles,'tag':tags,'category':categorys,'keyword':keywords})
    columns = ['title','time','area','tag','category','link','content','keyword']  #指定列的顺序
    dataframe.to_csv('result/'+dirname+'/news.csv',index=False,sep=',',columns=columns)
    return corpus

def LDA_topic(filename,begin_time,end_time,dirname):
    """
    LDA进行文档主题分析
    :param filename:原始文件路径
    :param begin_time:
    :param end_time:
    :param dirname:指定创建新目录名称
    :return:topic_list:每篇文档最有可能对应的两个topic
    """
    print('___________')
    print('LDA主题分析')
    topic_num = 10  # 聚类主题数目
    iter_num = 50  # 模型迭代次数

    if not os.path.exists('corpus/' + dirname + '/corpus.json'):  # 生成corpus
        print('开始生成语料库')
        corpus = get_corpus(filename, begin_time, end_time, dirname)
    else:
        print('此语料库已存在，直接加载')
    with open('corpus/' + dirname + '/corpus.json', 'r') as f:
        corpus = json.load(f)  # 加载语料库

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

    # 打印每篇文章所对应的topic
    for i in range(len(corpus)):
        print('******'+str(i)+'******')
        print(lda_topics[i])

    # 保存每篇文章最有可能所属的前3个topic类别
    topic_list = []
    for i in range(len(corpus)):
        t = ''
        #print('*******')
        topic_pr = map(lda_topics[i].tolist().index, heapq.nlargest(3, lda_topics[i]))
        topics = list(topic_pr)
        for j in range(len(topics)):
            t = t+str(topics[j])+','
        topic_list.append(t)

    data = pyLDAvis.sklearn.prepare(model, X, vect)
    #pyLDAvis.save_html(data, 'result/'+dirname+'/LDA.html')
    pyLDAvis.show(data)
    #print(topic_list)
    return topic_list

def kmeans_cluster(filename,begin_time,end_time,dirname):
    """
    k-means对文本进行聚类
    :param filename:原始文件路径
    :param begin_time:
    :param end_time:
    :param dirname:指定创建新目录名称
    :return:label_list:每篇文档所属的簇
    """

    print('________________')
    print('开始Kmeans聚类')

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

    print('**************文本向量*****************')
    print(X)

    clf = KMeans(n_clusters=10)  # 自定义聚类的簇
    clf.fit(X)

    label_list = []
    i = 1
    while i <= len(clf.labels_):  # 每个样本所属的簇
        label_list.append(clf.labels_[i - 1])
        i = i + 1

    #print(clf.inertia_)
    return label_list

def process(filename,begin_time,end_time,dirname):
    """
    先对文本进行LDA主题提取，再进行kmeans聚类，存储结果
    :param filename:原始文件路径
    :param begin_time:
    :param end_time:
    :param dirname:指定创建新目录名称
    :return:
    """
    topic_list = LDA_topic(filename,begin_time,end_time,dirname)
    label_list = kmeans_cluster(filename,begin_time,end_time,dirname)
    csv_data = pd.read_csv('result/' + dirname + '/news.csv')
    contents = csv_data['content']
    times = csv_data['time']
    titles = csv_data['title']
    links = csv_data['link']
    areas = csv_data['area']
    tags = csv_data['tag']
    categorys = csv_data['category']
    keywords = csv_data['keyword']

    # 存储结果
    dataframe = pd.DataFrame(
        {'time': times, 'link': links, 'area': areas, 'content': contents, 'title': titles, 'topic': topic_list,
         'tag': tags, 'category': categorys, 'label': label_list, 'keyword': keywords})
    columns = ['title', 'time', 'area', 'tag', 'category', 'link', 'content', 'keyword', 'topic', 'label']  # 指定列的顺序
    dataframe.to_csv('result/' + dirname + '/news.csv', index=False, sep=',', columns=columns)

def text_keyword(text,topK):
    #jieba.analyse.set_stop_words("settings/stop_words.txt")  # 加载自定义停用词表
    keywords = jieba.analyse.textrank(text, topK=topK, allowPOS=('n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd'))  # TextRank关键词提取，词性筛选
    word_split = " ".join(keywords)
    #print(word_split)
    return word_split

def show_result(filename):
    """
    查看kmeans的聚类效果
    :param filename:生成的结果文件路径
    :return:
    """
    print(filename)
    data = pd.read_csv(filename)
    topics = data['topic']
    labels = data['label']
    keywords = data['keyword']

    for i in range(15):
        print(i)
        content = ''
        for j in range(len(data)):
            if labels[j] == i:
                content = content + keywords[j]
        cluster_keywords = text_keyword(content, 5)
        print(cluster_keywords)


if __name__ == '__main__':
    # process('data/shipin_keywords.csv', '2018-1-1', '2018-2-1', '1月')
    # process('data/shipin_keywords.csv', '2018-2-1', '2018-3-1', '2月')
    # process('data/shipin_keywords.csv', '2018-3-1', '2018-4-1', '3月')
    # process('data/shipin_keywords.csv', '2018-4-1', '2018-5-1', '4月')
    # process('data/shipin_keywords.csv', '2018-5-1', '2018-6-1', '5月')
    # process('data/shipin_keywords.csv', '2018-6-1', '2018-7-1', '6月')
    # process('data/shipin_keywords.csv', '2018-7-1', '2018-8-1', '7月')
    # process('data/shipin_keywords.csv', '2018-8-1', '2018-9-1', '8月')
    # process('data/shipin_keywords.csv', '2018-9-1', '2018-10-1', '9月')
    # process('data/shipin_keywords.csv', '2018-10-1', '2018-11-1', '10月')
    # process('data/shipin_keywords.csv', '2018-11-1', '2018-12-1', '11月')
    # process('data/shipin_keywords.csv', '2018-12-1', '2018-12-31', '12月')
    # process('data/shipin_keywords.csv', '2018-1-1', '2018-12-1', '2018年')

    show_result('文本处理/文本聚类/result/2018年上/15_news.csv')
    show_result('文本处理/文本聚类/result/2018年下/15_news.csv')
    #LDA_topic('data/shipin_keywords.csv', '2018-1-1', '2018-12-31', '2018年')

    #kmeans_cluster('data/shipin_keywords.csv', '2018-1-1', '2018-2-1', '1月')
