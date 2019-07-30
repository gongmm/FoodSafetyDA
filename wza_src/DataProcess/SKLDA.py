# -*- coding: utf-8 -*-
import csv
import sys

from sklearn.decomposition import LatentDirichletAllocation
from time import time
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.externals import joblib
import matplotlib.pyplot as plt

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
            corpus.append(line.strip())
    print(len(corpus))


def save_topic_word(writefile='result/food_topic_word_sk.csv'):
    """将话题关键词存入单独的csv文件 ['topic_id', 'topic_word']
        Args:
            writefile : 写入的文件路径
    """
    lda = joblib.load(lda_model_file)
    # 主题-词分布
    tf_feature_names = joblib.load(feature_names_model_file)
    if lda is None or tf_feature_names is None:
        return
    for topic_idx, topic in enumerate(lda.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([tf_feature_names[i]
                             for i in topic.argsort()[:-n_topic - 1:-1]])
    with open(writefile, 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['topic_id', 'topic_word'])
        for topic_idx, topic in enumerate(lda.components_):
            topic_words = " ".join([tf_feature_names[i]
                                    for i in topic.argsort()[:-n_topic - 1:-1]])
            csv_writer.writerow([topic_idx, topic_words])


def write_doc_topic_to_origin(readfile='all_news_data_utf.csv', writefile='result/all_news_data_utf_topic_sk.csv'):
    """ 打印lda主题词 """
    lda_model = joblib.load(lda_model_file)
    doc_topic_dist = joblib.load(sk_doc_topic_file)
    tf_feature_names = joblib.load(feature_names_model_file)

    if lda_model is None:
        return
    # 主题-词分布
    # topic_word = lda_model.topic_word_
    for topic_idx, topic in enumerate(lda_model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([tf_feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

    print("type(doc_topic):{}".format(type(doc_topic_dist)))
    print("shape:{}".format(doc_topic_dist.shape))
    with open(readfile, 'r', encoding='utf-8') as f_read:
        rows = csv.reader(f_read)
        with open(writefile, 'w', encoding='utf-8', newline='') as f_write:
            writer = csv.writer(f_write)
            n = 0
            for row in rows:
                if n == 0:
                    topic_most_pr = 'topic_id'
                    row.append(topic_most_pr)
                    # 添加行
                    writer.writerow(row)
                # elif n <= 10000:
                else:
                    # 选择最可能的主题，对文档进行标记
                    topic_most_pr = doc_topic_dist[n - 1].argmax()
                    row.append(topic_most_pr)
                    writer.writerow(row)
                n = n + 1


def draw_doc_topic():

    doc_topic_dist = joblib.load(sk_doc_topic_file)
    if doc_topic_dist is None:
        return
    f, ax = plt.subplots(5, 1, figsize=(8, 6))
    for i, k in enumerate([1, 3, 4, 8, 9]):
        ax[i].stem(doc_topic_dist[k, :], linefmt='r-',
                   markerfmt='ro', basefmt='w-')
        ax[i].set_xlim(0, n_topic)
        ax[i].set_ylim(0, 1)
        ax[i].set_ylabel("Prob")
        ax[i].set_title("Document {}".format(k))

    ax[4].set_xlabel("Topic")

    plt.tight_layout()
    plt.show()
    # 保存图片
    plt.savefig('result/doc_topic_sk.png', bbox_inches='tight', pad_inches=0.1)


def sklearn_lda_train():
    """利用 sklearn 中的 lda 模型进行训练"""
    print("Loading dataset...")
    t0 = time()
    get_corpus()
    print("done in %0.3fs." % (time() - t0))
    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                    max_features=2000,
                                    stop_words='english')
    t0 = time()
    tf = tf_vectorizer.fit_transform(corpus)
    print("done in %0.3fs." % (time() - t0))
    print()
    print("======开始sklean_LDA=====")
    lda = LatentDirichletAllocation(n_components=n_topic, max_iter=10,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    t0 = time()
    lda.fit(tf)
    print("done in %0.3fs." % (time() - t0))

    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    joblib.dump(tf_feature_names, feature_names_model_file)
    for topic_idx, topic in enumerate(lda.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([tf_feature_names[i]
                             for i in topic.argsort()[:-n_topic - 1:-1]])
        print(message)
    print()

    t0 = time()
    doc_topic_dist = lda.transform(tf)
    joblib.dump(lda, lda_model_file)
    joblib.dump(doc_topic_dist, sk_doc_topic_file)
    print("done in %0.3fs." % (time() - t0))
    print("lda perplexity %.3f" % lda.perplexity(tf))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        sklearn_lda_train()
    save_topic_word()
    write_doc_topic_to_origin()
    draw_doc_topic()
