import csv

import jieba

''' 保存为txt文件：提取出指定话题的新闻信息的分词结果'''


def read_dir_file(readfile, writefile, topic_id):
    with open(readfile, 'r', encoding='utf-8-sig') as fr:
        rows = csv.DictReader(fr)
        # out = open(writefile, 'w', newline='', encoding='utf-8')
        # csv_writer = csv.writer(out, dialect='excel')
        out = open(writefile, 'w', encoding='utf-8')
        for row in rows:
            if row['topicid'] == str(topic_id):
                weibo_content = row['content']
                import re
                # 去掉数字：将0-9替换为‘’
                res = re.sub('[０-９]', '', weibo_content)
                # 微博内容的分词结果
                row_list = [eachWord for eachWord in jieba.cut(res)]  # 分词
                # 每条微博内容去掉停用词后的结果
                word_list = []
                '''停用词处理'''
                stop_words = open('../corpus/stopwords-utf8.txt', 'r', encoding='utf-8').read()
                for each_word in row_list:
                    if each_word not in stop_words and each_word != '\t' and each_word != ' ':
                        word_list.append(each_word)
                # 将处理后的内容去掉制表符写入新文件
                line = ''
                for index in range(len(word_list)):
                    if word_list[index].encode('utf-8') == '\n' or word_list[index].encode('utf-8') == 'nbsp' or \
                            word_list[index].encode('utf-8') == '\r\n':
                        continue
                    line += word_list[index]
                    line += ' '
                out.write(line)
                out.write('\n')


if __name__ == '__main__':
    for i in range(106):
        read_dir_file('../csv/testcsv/weiboshipin.csv', '../txt/weibo/weiboshipin_topic' + str(i) + '.txt', i)
