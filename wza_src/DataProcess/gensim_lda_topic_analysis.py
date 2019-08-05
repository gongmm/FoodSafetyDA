import codecs
from time import time
from gensim import corpora
from gensim.models import LdaModel
from gensim import models
from gensim.corpora import Dictionary
import sys
from sklearn.externals import joblib

n_topic = 36
corpus_file = 'corpus/news_content_corpus.txt'
lda_model_file = 'model/lda_gensim.model'
feature_names_model_file = 'model/features_gensim.model'
doc_topic_dist_file = 'model/doc_topic_gensim.model'
n_top_words = 20  # 选取的关键词个数
sk_doc_topic_file = 'model/gensim_doc_topic.model'


def get_corpus():
    """ 读取txt文件里面的内容建立语料库"""
    corpus = []
    with open(corpus_file, 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            corpus.append(line.strip().split())
            # corpus.append([line.strip()])
    print(len(corpus))
    print("To Dictionary...")
    t0 = time()
    dictionary = corpora.Dictionary(corpus)
    common_corpus = [dictionary.doc2bow(text) for text in corpus]
    print("done in %0.3fs." % (time() - t0))
    return dictionary, common_corpus


def gensim_lda_train():
    print("Loading dataset...")
    t0 = time()
    dictionary, common_corpus = get_corpus()
    print("done in %0.3fs." % (time() - t0))

    print("TF-IDF...")
    t0 = time()
    tfidf = models.TfidfModel(common_corpus)
    corpus_tfidf = tfidf[common_corpus]
    print("done in %0.3fs." % (time() - t0))
    print("Run the LDA model ...")
    t0 = time()
    lda = LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=n_topic, passes=10)
    print("done in %0.3fs." % (time() - t0))
    joblib.dump(lda, lda_model_file)
    # doc_topic = [a for a in lda[corpus]]
    # topics_r = lda.print_topics(num_topics=n_topic, num_words=n_top_words)


def print_info():
    dictionary, common_corpus = get_corpus()
    lda = joblib.load(lda_model_file)
    doc_topic = lda.get_document_topics(common_corpus)
    topics = lda.print_topics(num_topics=n_topic, num_words=n_top_words)

    for topic in topics:
        print(topic)

    # 打印每篇文档最高概率主题
    for i in lda.get_document_topics(common_corpus)[:]:
        listj = []
        for j in i:
            listj.append(j[1])
        bz = listj.index(max(listj))

        # print(i[bz][0],i,listj,listj.index(max(listj)))
        print(i[bz][0])

    # corpus_lda = lda[common_corpus]  # 每个文本对应的LDA向量，稀疏的，元素值是隶属与对应序数类的权重
    # num = 0
    # for doc in corpus_lda:
    #     wstr = ""
    #     for i in range(len(doc)):
    #         item = doc[i]
    #         wstr += str(item[0]) + "," + str(item[1])[0:7] + "/"
    #     num += 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        gensim_lda_train()
    print_info()
