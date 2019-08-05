# -*- coding: utf-8 -*-

from gensim.models import word2vec
import logging

from sklearn.externals import joblib

corpus = []
word2vec_model_file_100 = 'model/word2vec_100.model'
word2vec_model_file_50 = 'model/word2vec_50.model'
corpus_file = 'corpus/news_content_corpus.txt'


def get_corpus():
    """ 读取txt文件里面的内容建立语料库"""
    with open(corpus_file, 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            corpus.append([line.strip()])
    print(len(corpus))
    return corpus


def train():
    corpus = get_corpus()
    # 训练模型，部分参数如下
    sentences = word2vec.Text8Corpus(corpus_file)
    model = word2vec.Word2Vec(sentences, size=50, hs=1, min_count=1, window=3)
    model.save(word2vec_model_file_50)


def evaluate():
    print('-----------------模型预测----------------------------')
    # 加载模型
    model = word2vec.Word2Vec.load(word2vec_model_file_50)
    array = model.wv[u'三小']
    # 计算两个词向量的相似度
    try:
        sim1 = model.similarity(u'黑作坊', u'小作坊')
        sim2 = model.similarity(u'猪瘟', u'瘦肉精')
        most_similar_1 = model.most_similar('三无')
        most_similar_2 = model.most_similar('北京')

    except KeyError:
        sim1 = 0
        sim2 = 0
        most_similar_1 = []
        most_similar_2 = []
    print(u'黑作坊 和 小作坊 的相似度为 ', sim1)
    print(u'猪瘟 和 瘦肉精 的相似度为 ', sim2)
    print('=====与“三无”最相似的词=====')
    for item in most_similar_1:
        print(u'三无 ', item)
    print('=====与“北京”最相似的词=====')
    for item in most_similar_2:
        print(u'北京 ', item)


if __name__ == '__main__':
    # train()
    evaluate()
