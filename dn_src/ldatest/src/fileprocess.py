# -*- coding: utf-8 -*-
import csv
import jieba
import sys
import os


# reload(sys)
# sys.setdefaultencoding('utf8')
class fileprocess:
    """
    读取csv保存为单独的txt文件
    将csv中的每一行保存为txt/*/nlp_test_i.txt文件
    """

    def gongye(self):
        with open('./csv/triancsv/peoplenews_result_204.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            content_list = [row['content'] for row in reader]
            i = 1
            for content in content_list:
                # print content
                # content_decode=content.decode('GBK')
                documnet_cut = jieba.cut(content)
                result = ''.join(documnet_cut)
                result.encode('utf-8')
                with open('./txt/gongye/nlp_test' + str(i) + '.txt', 'w', encoding='utf-8') as f2:
                    f2.write(result)
                    f2.close()
                i = i + 1
        csvfile.close()

    '''读取csv并保存为单独的txt文件'''

    def sanju(self):
        with open('./csv/triancsv/peoplenews_result_516.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            content_list = [row['content'] for row in reader]
            i = 1
            for content in content_list:
                # print content
                # content_decode=content.decode('GBK')
                documnet_cut = jieba.cut(content)
                result = ''.join(documnet_cut)
                result.encode('utf-8')
                with open('./txt/sanju/nlp_test' + str(i) + '.txt', 'w', encoding='utf-8') as f2:
                    f2.write(result)
                    f2.close()
                i = i + 1
        csvfile.close()

    '''读取csv并保存为单独的txt文件'''

    def suhuaji(self):
        with open('./csv/triancsv/peoplenews_result_344.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            content_list = [row['content'] for row in reader]
            i = 1
            for content in content_list:
                # print content
                # content_decode=content.decode('GBK')
                documnet_cut = jieba.cut(content)
                result = ''.join(documnet_cut)
                result.encode('utf-8')
                with open('./txt/suhuaji/nlp_test' + str(i) + '.txt', 'w', encoding='utf-8') as f2:
                    f2.write(result)
                    f2.close()
                i = i + 1
        csvfile.close()

    '''读取csv并保存为单独的txt文件'''

    def gedami(self):
        with open('./csv/triancsv/peoplenews_result_97.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            content_list = [row['content'] for row in reader]
            i = 1
            for content in content_list:
                # print content
                # content_decode=content.decode('GBK')
                documnet_cut = jieba.cut(content)
                result = ''.join(documnet_cut)
                result.encode('utf-8')
                with open('./txt/gedami/nlp_test' + str(i) + '.txt', 'w', encoding='utf-8') as f2:
                    f2.write(result)
                    f2.close()
                i = i + 1
        csvfile.close()

    '''读取csv并保存为单独的txt文件'''

    def digouyou(self):
        with open('./csv/triancsv/peoplenews__result_381.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            content_list = [row['content'] for row in reader]
            i = 1
            for content in content_list:
                # print content
                # content_decode=content.decode('GBK')
                documnet_cut = jieba.cut(content)
                result = ''.join(documnet_cut)
                result.encode('utf-8')
                with open('./txt/digouyou/nlp_test' + str(i) + '.txt', 'w', encoding='utf-8') as f2:
                    f2.write(result)
                    f2.close()
                i = i + 1
        csvfile.close()

    '''读取csv并将每一列保存为单独的txt文件'''

    def dudouya(self):
        with open('./csv/triancsv/peoplenews_result_53.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            content_list = [row['content'] for row in reader]
            i = 1
            for content in content_list:
                # content_decode=content.decode('unicode-escape')
                documnet_cut = jieba.cut(content)
                result = ''.join(documnet_cut)
                result.encode('utf-8')
                with open('./txt/dudouya/nlp_test' + str(i) + '.txt', 'w', encoding='utf-8') as f2:
                    f2.write(result)
                    f2.close()
                i = i + 1
        csvfile.close()

    '''读取csv并保存为单独的txt文件'''

    def shouroujing(self):
        with open('./csv/triancsv/peoplenews_result_344.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            content_list = [row['content'] for row in reader]
            i = 1
            for content in content_list:
                # print content
                # content_decode=content.decode('GBK')
                documnet_cut = jieba.cut(content)
                result = ''.join(documnet_cut)
                result.encode('utf-8')
                with open('./txt/shouroujing/nlp_test' + str(i) + '.txt', 'w', encoding='utf-8') as f2:
                    f2.write(result)
                    f2.close()
                i = i + 1
        csvfile.close()

    '''读取csv并保存为单独的txt文件'''

    def shipin_test(self):
        with open('../csv/testcsv/shipinprocess.csv', newline='', encoding='UTF-8') as csvfile:
            reader = csv.DictReader(csvfile)
            content_list = [row['content'] for row in reader]
            i = 0
            for content in content_list:
                documnet_cut = jieba.cut(content)
                result = ''.join(documnet_cut)
                result.encode('utf-8')
                with open('../txt/shipintest/nlp_test' + str(i) + '.txt', 'w', encoding='utf-8', newline='') as f2:
                    f2.write(content)
                    f2.close()
                i = i + 1
        csvfile.close()

    # 遍历指定目录，显示目录下的所有文件名
    def eachFile(self, filepath):
        pathDir = os.listdir(filepath)
        for allDir in pathDir:
            child = os.path.join('%s%s' % (filepath, allDir))
            # print child.decode('gbk')  # .decode('gbk')是解决中文显示乱码问题

    # 读取文件内容并打印
    def readFile(self, filename):
        fopen = open(filename, 'r')  # r 代表read
        res = fopen.read()
        return res
        fopen.close()

    '''读取文件目录下所有文件组合成语料并且将所有txt文档集合在一个文档中
    #1.进行分词
    #2.进行停用词的处理
    3.返回语料
    4.并将处理的txt文档集合在一个文档中
    '''

    def readdirFile(self, readfilepath, writefile):
        corpus = []
        pathDir = os.listdir(readfilepath)
        print(pathDir)
        for allDir in pathDir:
            child = os.path.join('%s%s' % (readfilepath, allDir))
            with open(child, encoding='utf-8') as f:
                res = f.read()
                # document3_cut = jieba.cut(res)#进行中文分词
                import re
                # 文档内容
                res = re.sub('[０-９]', '', res)
                rowList = [eachWord for eachWord in jieba.cut(res)]  # 分词
                wordList = []
                # 文档内容去掉停用词后的结果
                removeStopwordList = []
                '''停用词处理'''
                stopWords = open('../corpus/stopwords-utf8.txt', 'r', encoding='utf-8').read()
                for eachword in rowList:
                    if eachword not in stopWords and eachword != '\t' and eachword != ' ':
                        removeStopwordList.append(eachword)
                wordList.append(removeStopwordList)
                print("读取文件" + child)
                # # 将处理后的内容去掉制表符写入新文件
                line = ''
                for word in wordList:
                    for i in range(len(word)):
                        if word[i].encode('utf-8') == '\n' or word[i].encode('utf-8') == 'nbsp' or word[i].encode(
                                'utf-8') == '\r\n':
                            continue
                        line += word[i]
                        line += ' '
                    writefile.write(line + '\n')  # 把这行写进文件
                # 将分词结果加入语料库
                for i in range(len(wordList)):
                    wordList[i] = " ".join(wordList[i])
                    corpus.append(wordList[i])
                f.close()
        return corpus

    '''主题困惑度分析'''

    def topicAnalyze(self, corpus):
        from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
        from sklearn.decomposition import NMF, LatentDirichletAllocation
        import random
        from time import time

        train_size = int(round(len(corpus) * 0.8))  # 分解训练集和测试集
        train_index = sorted(random.sample(range(len(corpus)), train_size))  # 随机选取train_size个下标
        test_index = sorted(set(range(len(corpus))) - set(train_index))
        train_corpus = [corpus[i] for i in train_index]  # 训练集语料
        test_corpus = [corpus[j] for j in test_index]

        n_features = 2000
        n_top_words = 1000

        print("Extracting tf features for LDA...")
        # 选取至少出现过两次并且数量为前2000的单词用来生成文本表示向量
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=n_features,
                                        stop_words='english')
        t0 = time()
        # 使用向量生成器转化测试集
        tf = tf_vectorizer.fit_transform(train_corpus)
        print("done in %0.3fs." % (time() - t0))
        # Use tf (raw term count) features for LDA.
        print("Extracting tf features for LDA...")
        tf_test = tf_vectorizer.transform(test_corpus)
        print("done in %0.3fs." % (time() - t0))
        # 存储主题数以及对应的困惑度
        grid = dict()
        t0 = time()
        # 300个主题，以5为间隔
        for i in range(1, 300, 5):
            grid[i] = list()
            n_topics = i
            # 定义lda模型
            lda = LatentDirichletAllocation(n_components=n_topics, max_iter=5, learning_method='online',
                                            learning_offset=50., random_state=0)
            # 训练参数
            lda.fit(tf)
            # 得到topic-document 分布
            train_gamma = lda.transform(tf)
            train_perplexity = lda.perplexity(tf)
            # 计算测试集困惑度
            test_perplexity = lda.perplexity(tf_test)
            print('sklearn preplexity: train=%.3f' % (train_perplexity))
            grid[i].append(train_perplexity)

        print("done in %0.3fs." % (time() - t0))
        import pandas as pd
        from matplotlib import pyplot as plt
        df = pd.DataFrame(grid)
        df.to_csv('sklearn_perplexity.csv')
        print(df)
        plt.figure(figsize=(14, 8), dpi=120)
        # plt.subplot(221)
        plt.plot(df.columns.values, df.iloc[0].values, '#007A99')
        plt.xticks(df.columns.values)
        plt.ylabel('train Perplexity')
        plt.show()
        plt.savefig('lda_topic_perplexity.png', bbox_inches='tight', pad_inches=0.1)

    '''添加新列'''

    def addcols(self, colcontent):
        with open('./csv/testcsv/shipin_topic_1.csv', 'r', encoding='utf-8') as f:
            rows = csv.reader(f)
            with open('./csv/testcsv/shipin_topic_1.csv_new.csv', 'w', encoding='utf-8', newline='') as f1:
                writer = csv.writer(f1)
                for row in rows:
                    print(row)
                    # row = [row1.encode("utf-8") for row1 in row]
                    row.append(colcontent)
                    writer.writerow(row)


if __name__ == '__main__':
    # shipin_test()
    fileprocess = fileprocess()
    fileprocess.shipin_test()
    # writefile = open('../corpus/doc_shipin.txt', 'w', encoding='utf-8')  # 把所有的文本都集合在这个文档里
    # corpus=fileprocess.readdirFile('../txt/shipintest/',writefile)
    # print (len(corpus))
    # fileprocess.topicAnalyze(corpus)
    # readdirFile('./txt/digouyou/')
    # readdirFile('./txt/dudouya/')
    # readdirFile('./txt/gedami/')
    # readdirFile('./txt/gongye/')
    # readdirFile('./txt/sanju/')
    # readdirFile('./txt/shouroujing/')
    # readdirFile('./txt/suhuaji/')
    # topicAnalyze()
