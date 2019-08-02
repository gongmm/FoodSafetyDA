# -*- coding: utf-8 -*-

from gensim.models import word2vec
import logging

from sklearn.externals import joblib

corpus = []
word2vec_model_file = 'model/word2vec.model'
corpus_file='corpus/news_content_corpus.txt'


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
    model = word2vec.Word2Vec(sentences, size=100, hs=1, min_count=1, window=3)
    model.save(word2vec_model_file)


def evaluate():
    print('-----------------模型预测----------------------------')
    # 加载模型
    model = word2vec.Word2Vec.load(word2vec_model_file)

    # 计算两个词向量的相似度
    try:
        sim1 = model.similarity(u'黑作坊', u'小作坊')
        sim2 = model.similarity(u'猪瘟', u'瘦肉精')
    except KeyError:
        sim1 = 0
        sim2 = 0
    print(u'黑作坊 和 小作坊 的相似度为 ', sim1)
    print(u'猪瘟 和 瘦肉精 的相似度为 ', sim2)


if __name__ == '__main__':
    # train()
    evaluate()