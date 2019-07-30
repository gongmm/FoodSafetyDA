import codecs
from time import time
from gensim import corpora
from gensim.models import LdaModel
from gensim import models
from gensim.corpora import Dictionary

corpus = []
n_topic = 36
corpus_file = 'corpus/news_content_corpus.txt'
lda_model_file = 'model/lda_sk.model'
feature_names_model_file = 'model/features_sk.model'
doc_topic_dist_file = 'model/doc_topic_sk.model'
n_top_words = 20  # 选取的关键词个数
sk_doc_topic_file = 'model/sk_doc_topic.model'


def get_corpus():
    """ 读取txt文件里面的内容建立语料库"""
    with open(corpus_file, 'r', encoding='UTF-8') as file:
        for line in file.readlines():
            corpus.append(line.strip().split())
    print(len(corpus))


def gensim_lda_train():
    print("Loading dataset...")
    t0 = time()
    get_corpus()
    print("done in %0.3fs." % (time() - t0))
    print("To Dictionary...")
    t0 = time()
    dictionary = corpora.Dictionary(corpus)
    common_corpus = [dictionary.doc2bow(text) for text in corpus]
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
    doc_topic = [a for a in lda[corpus]]
    topics_r = lda.print_topics(num_topics=n_topic, num_words=n_top_words)


if __name__ == '__main__':
    gensim_lda_train()