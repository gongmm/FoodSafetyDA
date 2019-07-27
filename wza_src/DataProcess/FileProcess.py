# -*- coding: utf-8 -*-
import csv
import jieba
import os
import re


class FileProcess:
    """
    读取csv保存为单独的txt文件
    将csv中的每一行保存为txt/*/nlp_content_text_i.txt文件
    """

    @staticmethod
    def csv_to_single_txt(readfile, writefile):
        with open(readfile, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            content_list = [row['content'] for row in reader]
            i = 1
            for content in content_list:
                print(content)
                # content_decode=content.decode('GBK')
                document_cut = jieba.cut(content)
                result = ''.join(document_cut)
                result.encode('utf-8')
                with open(writefile + '/nlp_test' + str(i) + '.txt', 'w', encoding='utf-8') as txt_file:
                    txt_file.write(result)
                    txt_file.close()
                i = i + 1
        csv_file.close()

    # 遍历指定目录，显示目录下的所有文件名
    @staticmethod
    def display_file(filepath):
        path_dir = os.listdir(filepath)
        for all_dir in path_dir:
            child = os.path.join('%s%s' % (filepath, all_dir))
            print(child.decode('gbk'))  # .decode('gbk')是解决中文显示乱码问题

    # 读取文件内容并打印
    @staticmethod
    def read_file(filename):
        file = open(filename, 'r', encoding='utf-8')  # r 代表read
        res = file.read()
        file.close()
        return res

    '''读取文件目录下所有文件组合成语料并且将所有txt文档集合在一个文档中
    #1.进行分词
    #2.进行停用词的处理
    3.返回语料
    4.并将处理的txt文档集合在一个文档中
    '''

    @staticmethod
    def make_corpus_from_dir(root, write_path):
        writefile = open(write_path, 'w', encoding='utf-8')
        corpus = []
        path_dir = os.listdir(root)
        print(path_dir)
        for all_dir in path_dir:
            child = os.path.join('%s%s' % (root, all_dir))
            # 打开目录下包含的文档
            with open(child, encoding='utf-8') as child_file:
                res = child_file.read()
                res = re.sub('[０-９]', '', res)
                # 分词
                row_list = [eachWord for eachWord in jieba.cut(res)]
                # 文档内容去掉停用词后的结果
                word_list = []

                '''停用词处理'''
                stop_words = open('corpus/stopwords-utf8.txt', 'r', encoding='utf-8').read()
                for each_word in row_list:
                    if each_word not in stop_words and each_word != '\t' and each_word != ' ':
                        word_list.append(each_word)
                print("读取文件" + child)
                # 将处理后的内容去掉制表符写入新文件
                line = ''
                # for word in wordList:
                for i in range(len(word_list)):
                    if word_list[i].encode('utf-8') == '\n' or word_list[i].encode('utf-8') == 'nbsp' or \
                            word_list[i].encode('utf-8') == '\r\n':
                        continue
                    line += word_list[i]
                    line += ' '
                writefile.write(line + '\n')  # 把这行写进文件
                # 将分词结果加入语料库
                for i in range(len(word_list)):
                    word_list[i] = " ".join(word_list[i])
                    corpus.append(word_list[i])
        writefile.close()
        return corpus

    '''添加新列'''

    @staticmethod
    def add_cols(readfile, writefile, content):
        with open(readfile, 'r', encoding='utf-8') as f:
            rows = csv.reader(f)
            with open(writefile, 'w', encoding='utf-8', newline='') as f1:
                writer = csv.writer(f1)
                for row in rows:
                    print(row)
                    # row = [row1.encode("utf-8") for row1 in row]
                    row.append(content)
                    writer.writerow(row)


if __name__ == '__main__':
    # 把所有的文本都集合在这个food_news_corpus里
    # FileProcess.csv_to_single_txt('test.csv', 'data')
    FileProcess.make_corpus_from_dir('data/', 'corpus/test_corpus.txt')
    # corpus_result = FileProcess.make_corpus_from_dir('data/food_nlp_text/', 'corpus/food_news_corpus.txt')
    # print(len(corpus_result))

    # shipin_test()

    # readdirFile('./txt/digouyou/')
    # readdirFile('./txt/dudouya/')
    # readdirFile('./txt/gedami/')
    # readdirFile('./txt/gongye/')
    # readdirFile('./txt/sanju/')
    # readdirFile('./txt/shouroujing/')
    # readdirFile('./txt/suhuaji/')
    # topicAnalyze()
