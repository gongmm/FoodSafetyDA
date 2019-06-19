import csv
from os import listdir
import numpy as np
from os.path import join
import codecs
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import re
import pkuseg
'''
topic_shipin
提取topicid,docid
'''
def readtopictxt():
    with open('../doc_topic/doc_topic.txt','r',encoding='utf-8') as f:
        with open('./doc_topic/doc_topic.csv','w',encoding='utf-8',newline='') as csvffile:
            writer=csv.writer(csvffile)
            writer.writerow(['docid','topicid'])
            for line in f.readlines():
                docid=line.split()[1]
                topicid=line.split()[3]
                writer.writerow([docid,topicid])
import pymysql
import jieba
import os
class Doc2Vector():
    conn = pymysql.Connect(host="127.0.0.1", port=3306, user='root', password='123456', database='shipin',
                               charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    countsql='select count(distinct topicid) from doctopic '
    cursor.execute(countsql)
    topicdict=cursor.fetchone()
    topicnum=topicdict.get('count(distinct topicid)')
    '''
    采用jieba分词
    '''
    def gettopicdoc(self):
        for topicid in range(self.topicnum):
            sql='select * from doctopic where topicid='+str(topicid)
            self.cursor.execute(sql)
            doctuples = self.cursor.fetchall()
            print(doctuples)
            for i in range(len(doctuples)):
                with open('../txt/shipintest/nlp_test'+doctuples[i].get('docid')+'.txt','r',encoding='utf-8') as f:
                    isExists = os.path.exists('../txt/topic_doc_jieba/topic' + doctuples[i].get('topicid'))
                    # 判断结果
                    if not isExists:
                        # 如果不存在则创建目录 创建目录操作函数
                        os.makedirs('../txt/topic_doc_jieba/topic' + doctuples[i].get('topicid'))
                    #with open('../txt/topic_doc_jieba/nlp_topic'+doctuples[i].get('topicid')+'.txt','a+',encoding='utf-8') as fw:
                    with open('../txt/topic_doc_jieba/topic' + doctuples[i].get('topicid') + '/topic' + doctuples[i].get('topicid') + '_doc' + doctuples[i].get('docid') + '.txt', 'w',
                                  encoding='utf-8') as fw:
                        txtcontent=f.read()
                        rowList = [eachWord for eachWord in jieba.cut(txtcontent)]  # 分词
                        wordList = []
                        removeStopwordList = []
                        '''停用词处理'''
                        stopWords = open('../corpus/stopwords-utf8.txt', 'r', encoding='utf-8').read()
                        for eachword in rowList:
                            if eachword not in stopWords and eachword != '\t' and eachword != ' ':
                                removeStopwordList.append(eachword)
                        wordList.append(removeStopwordList)
                    # 写入文件
                        line = ''
                        for word in wordList:
                            for i in range(len(word)):
                                if word[i].encode('utf-8') == '\n' or word[i].encode('utf-8') == 'nbsp' or word[i].encode(
                                        'utf-8') == '\r\n':
                                    continue
                                line += word[i]
                                line += ' '
                            print(line)
                            fw.write(line + '\n')  # 把这行写进文件
    '''
     存储每个topic下所有的doc
    #分词、去停用词
    #采用 pkuseg北大
    '''
    def gettopicdoc2(self):
        conn=pymysql.Connect(host="127.0.0.1",port=3306,user='root',password='123456',database='shipin',charset='utf8')
        cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
        seg = pkuseg.pkuseg()  # 以默认配置加载模型
        for topicid in range(self.topicnum):
            sql='select * from doctopic where topicid='+str(topicid)
            cursor.execute(sql)
            doctuples = cursor.fetchall()
            print(doctuples)
            for i in range(len(doctuples)):
                with open('../txt/shipintest/nlp_test'+doctuples[i].get('docid')+'.txt','r',encoding='utf-8') as f:
                    isExists = os.path.exists('../txt/topic_doc_pk/topic'+doctuples[i].get('topicid'))
                    # 判断结果
                    if not isExists:
                        # 如果不存在则创建目录 创建目录操作函数
                        os.makedirs('../txt/topic_doc_pk/topic'+doctuples[i].get('topicid'))
                    with open('../txt/topic_doc_pk/topic'+doctuples[i].get('topicid')+'/topic'+doctuples[i].get('topicid')+'_doc'+doctuples[i].get('docid')+'.txt','w',encoding='utf-8') as fw:
                        doc = f.read()
                        reg_html = re.compile(r'<[^>]+>', re.S)
                        doc = reg_html.sub('', doc)
                        doc = re.sub('[０-９]', '', doc)
                        doc = re.sub('\s', '', doc)
                        rowList = [eachWord for eachWord in seg.cut(doc)]  # 分词
                        wordList = []
                        removeStopwordList = []
                        '''停用词处理'''
                        stopWords = open('../corpus/stopwords-utf8.txt', 'r', encoding='utf-8').read()
                        for eachword in rowList:
                            if eachword not in stopWords and eachword != '\t' and eachword != ' ':
                                removeStopwordList.append(eachword)
                        wordList.append(removeStopwordList)
                        # 写入文件
                        line = ''
                        for word in wordList:
                            for i in range(len(word)):
                                if word[i].encode('utf-8') == '\n' or word[i].encode('utf-8') == 'nbsp' or word[i].encode(
                                        'utf-8') == '\r\n':
                                    continue
                                line += word[i]
                                line += ' '
                            print(line)
                            fw.write(line + '\n')  # 把这行写进文件
        cursor.close()
        conn.close()

    def train(self):
        """训练 并保存Doc2Vec 模型
        """
        for n in range(self.topicnum):
            # 先把所有文档的路径存进一个 array中，docLabels：
            data_dir = "../txt/topic_doc_pk/topic" + str(n)
            docLabels = [f for f in listdir(data_dir) if f.endswith('.txt')]

            data = []
            for doc in docLabels:
                ws = open(data_dir + "/" + doc, 'r', encoding='UTF-8').read()
                data.append(ws)

            print(len(data))
            # 训练 Doc2Vec，并保存模型：
            sentences = LabeledLineSentence(data, docLabels)
            # an empty model
            model = gensim.models.Doc2Vec(vector_size=256, window=8, min_count=3,
                                          workers=4, alpha=0.025, min_alpha=0.025, epochs=12)
            model.build_vocab(sentences)
            print("开始训练...")
            model.train(sentences, total_examples=model.corpus_count, epochs=12)
            # train doc2vec model

            # save model
            model.save("../models/doc2vec" + str(n) + ".model")
            print("model saved")

    def test_model(self):
        for n in range(self.topicnum):
            print("load model")
            model = gensim.models.Doc2Vec.load('../models/doc2vec'+str(n)+'.model')

            data_dir = "../txt/topic_doc_pk/topic" + str(n)
            docLabels = [f for f in listdir(data_dir) if f.endswith('.txt')]
            print (len(docLabels))
            st1=""
            st2 =""
            with open('../simlarity/topic' + str(n) + '.csv', 'w') as csvffile:
                writer = csv.writer(csvffile)
                writer.writerow(["docid", "similarity"])
                for i in range(len(docLabels)):
                    ws = open(data_dir + "/" + docLabels[i], 'r', encoding='UTF-8').read()  # 一行文件
                    list1=ws.split()
                    for doc in docLabels:
                        if doc!=docLabels[i]:
                            ws = open(data_dir + "/" + doc, 'r', encoding='UTF-8').read()#一行文件
                            st2=st2+ws
                    list2=st2.split()
                    print(docLabels[i])
                    # 转成句子向量
                    vect1 = self.sent2vec(model, list1)
                    vect2 = self.sent2vec(model, list2)

                    # 查看变量占用空间大小
                    import sys
                    print(sys.getsizeof(vect1))
                    print(sys.getsizeof(vect2))

                    cos = similarity(vect1, vect2)
                    print("相似度：{:.4f}".format(cos))
                    docid=docLabels[i].split('doc')[1].split('.')[0]
                    writer.writerow([docid,cos])
    def testtopic12(self):
        n=103
        model = gensim.models.Doc2Vec.load('../models/doc2vec' + str(n) + '.model')

        data_dir = "../txt/topic_doc_pk/topic" + str(n)
        docLabels = [f for f in listdir(data_dir) if f.endswith('.txt')]
        #print(len(docLabels))
        st1 = ""
        st2 = ""
        with open('../simlarity/topic' + str(n) + '.csv', 'w') as csvffile:
            writer = csv.writer(csvffile)
            writer.writerow(["docid", "similarity"])
            for i in range(len(docLabels)):
                ws = open(data_dir + "/"+docLabels[i] , 'r', encoding='UTF-8').read()  # 一行文件
                st1 = ws
                list1=st1.split()
                for doc in docLabels:
                    if doc != docLabels[i]:
                        ws = open(data_dir + "/" + doc, 'r', encoding='UTF-8').read()  # 一行文件
                        st2 = st2 + ws
                list2=st2.split()
                print(docLabels[i])
                # 转成句子向量
                vect1 = self.sent2vec(model, list1)
                vect2 = self.sent2vec(model, list2)
                # 查看变量占用空间大小
                import sys
                print(sys.getsizeof(vect1))
                print(sys.getsizeof(vect2))

                cos = similarity(vect1, vect2)
                print("相似度：{:.4f}".format(cos))
                docid = docLabels[i].split('doc')[1].split('.')[0]
                writer.writerow([docid, cos])




    def similarity(self,a_vect, b_vect):
        """计算两个向量余弦值

        Arguments:
            a_vect {[type]} -- a 向量
            b_vect {[type]} -- b 向量

        Returns:
            [type] -- [description]
        """

        dot_val = 0.0
        a_norm = 0.0
        b_norm = 0.0
        cos = None
        for a, b in zip(a_vect, b_vect):
            dot_val += a * b
            a_norm += a ** 2
            b_norm += b ** 2
        if a_norm == 0.0 or b_norm == 0.0:
            cos = -1
        else:
            cos = dot_val / ((a_norm * b_norm) ** 0.5)

        return cos

    def sent2vec(self,model, words):
        """文本转换成向量

        Arguments:
            model {[type]} -- Doc2Vec 模型
            words {[type]} -- 分词后的文本

        Returns:
            [type] -- 向量数组
        """
        vect_list = []
        for w in words:
            try:
                vect_list.append(model.wv[w])
            except Exception as e:
                #print(e)
                continue
        vect_list = np.array(vect_list)
        vect = vect_list.sum(axis=0)
        return vect / np.sqrt((vect ** 2).sum())
    def __del__(self):
        print("析构函数被调用")
        self.cursor.close()
        self.conn.close()

def doc_segment():
        """分词保存
        """

        # 先把所有文档的路径存进一个 array 中，docLabels：
        data_dir = "./data/corpus"
        docLabels = [f for f in listdir(data_dir) if f.endswith('.txt')]

        data = []
        for doc in docLabels:
            try:
                ws = codecs.open(data_dir + "/" + doc).read()
                doc_words = segment(ws)
                with codecs.open("data/corpus_words/{}".format(doc), "a", encoding="UTF-8") as f:
                    f.write(" ".join(doc_words))
            except:
                print(doc)


def segment(doc,str):
        """中文分词
        Arguments:
            doc {str} -- 输入文本
        Returns:
            [type] -- [description]
        """
        # 停用词
        stop_words = pd.read_csv("./data/stopwords_TUH.txt", index_col=False, quoting=3,
                                 names=['stopword'],
                                 sep="\n",
                                 encoding='utf-8')
        stop_words = list(stop_words.stopword)

        reg_html = re.compile(r'<[^>]+>', re.S)
        doc = reg_html.sub('', doc)
        doc = re.sub('[０-９]', '', doc)
        doc = re.sub('\s', '', doc)
        word_list = list(jieba.cut(doc))
        out_str = ''
        for word in word_list:
            if word not in stop_words:
                out_str += word
                out_str += ' '
        segments = out_str.split(sep=" ")

        return segments

def test_model():
        print("load model")
        model = gensim.models.Doc2Vec.load('./models/doc2vec.model')

        st1 = open('./data/courpus_test/t1.txt', 'r', encoding='UTF-8').read()
        st2 = open('./data/courpus_test/t2.txt', 'r', encoding='UTF-8').read()
        # 分词
        print("segment")
        st1 = segment(st1)
        st2 = segment(st2)
        # 转成句子向量
        vect1 = sent2vec(model, st1)
        vect2 = sent2vec(model, st2)

        # 查看变量占用空间大小
        import sys
        print(sys.getsizeof(vect1))
        print(sys.getsizeof(vect2))

        cos = similarity(vect1, vect2)
        print("相似度：{:.4f}".format(cos))


def similarity(a_vect, b_vect):
        """计算两个向量余弦值

        Arguments:
            a_vect {[type]} -- a 向量
            b_vect {[type]} -- b 向量

        Returns:
            [type] -- [description]
        """

        dot_val = 0.0
        a_norm = 0.0
        b_norm = 0.0
        cos = None
        for a, b in zip(a_vect, b_vect):
            dot_val += a * b
            a_norm += a ** 2
            b_norm += b ** 2
        if a_norm == 0.0 or b_norm == 0.0:
            cos = -1
        else:
            cos = dot_val / ((a_norm * b_norm) ** 0.5)

        return cos


def sent2vec(model, words):
        """文本转换成向量

        Arguments:
            model {[type]} -- Doc2Vec 模型
            words {[type]} -- 分词后的文本

        Returns:
            [type] -- 向量数组
        """

        vect_list = []
        for w in words:
            try:
                vect_list.append(model.wv[w])
            except:
                continue
        #print(vect_list)
        vect_list = np.array(vect_list)
        vect = vect_list.sum(axis=0)
        return vect / np.sqrt((vect ** 2).sum())


class LabeledLineSentence(object):
        def __init__(self, doc_list, labels_list):
            self.labels_list = labels_list
            self.doc_list = doc_list

        def __iter__(self):
            for idx, doc in enumerate(self.doc_list):
                yield gensim.models.doc2vec.LabeledSentence(words=doc.split(), tags=[self.labels_list[idx]])
if __name__=="__main__":
    doc=Doc2Vector()
    #doc.testtopic12()
    #doc.gettopicdoc()
    #doc.train()
    #doc.gettopicdoc2()
    #doc.test_model()
    doc.testtopic12()


