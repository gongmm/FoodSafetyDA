import os
import csv

import jieba

''' 保存为txt文件'''


def readdirFile(readfilepath, writefile, topicid):
    with open(readfilepath, 'r', encoding='utf-8-sig') as fr:
        rows = csv.DictReader(fr)
        # out = open(writefile, 'w', newline='', encoding='utf-8')
        # csv_writer = csv.writer(out, dialect='excel')
        out = open(writefile, 'w', encoding='utf-8')
        for row in rows:
            if row['topicid'] == str(topicid):
                weiboContent = row['content']
                import re
                # 每一条微博内容
                res = re.sub('[０-９]', '', weiboContent)
                # 微博内容的分词结果
                rowList = [eachWord for eachWord in jieba.cut(res)]  # 分词
                wordList = []
                # 每条微博内容去掉停用词后的结果
                removeStopWordList = []
                '''停用词处理'''
                stopWords = open('../corpus/stopwords-utf8.txt', 'r', encoding='utf-8').read()
                for eachWord in rowList:
                    if eachWord not in stopWords and eachWord != '\t' and eachWord != ' ':
                        removeStopWordList.append(eachWord)
                wordList.append(removeStopWordList)
                # 将处理后的内容去掉制表符写入新文件
                line = ''
                for word in wordList:
                    for i in range(len(word)):
                        if word[i].encode('utf-8') == '\n' or word[i].encode('utf-8') == 'nbsp' or word[i].encode(
                                'utf-8') == '\r\n':
                            continue
                        line += word[i]
                        line += ' '
                    # csv_writer.writerow(word)
                    out.write(line)
                    out.write('\n')


''' 保存为csv文件'''


def readfiletocsv(readfilepath, writefile):
    with open(readfilepath, 'r', encoding='utf-8') as fr:
        rows = csv.DictReader(fr)
        out = open(writefile, 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(out, dialect='excel')
        for row in rows:
            if row['topicid'] == '4':
                weibocontent = row['content']
                import re
                res = re.sub('[０-９]', '', weibocontent)
                rowList = [eachWord for eachWord in jieba.cut(res)]  # 分词
                wordList = []
                removeStopwordList = []
                '''停用词处理'''
                stopWords = open('../corpus/stopwords-utf8.txt', 'r', encoding='utf-8').read()
                for eachword in rowList:
                    if eachword not in stopWords and eachword != '\t' and eachword != ' ':
                        removeStopwordList.append(eachword)
                wordList.append(removeStopwordList)
                line = ''
                for word in wordList:
                    csv_writer.writerow(word)


if __name__ == '__main__':
    for i in range(106):
        readdirFile('../csv/testcsv/weiboshipin.csv', '../txt/weibo/weiboshipin_topic' + str(i) + '.txt', i)
