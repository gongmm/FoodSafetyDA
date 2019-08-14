from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import random
from time import time
import pandas as pd
from matplotlib import pyplot as plt


def get_corpus(filepath):
    """读取txt文件里面的内容保存为语料

    Args:
        filepath: 读取corpus.txt所在的路径
    """
    corpus = []
    with open(filepath, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            corpus.append(line.strip())
    print(len(corpus))
    return corpus


def topic_analyze(corpus):
    """
    确定主题数
    Args:
        corpus:

    Returns:

    """
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
    for i in range(30, 60, 5):
        print("===== calculate topic num %d =====" % i)
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
        print('sklearn preplexity: train=%.3f , test:%.3f' % (train_perplexity, test_perplexity))
        grid[i].append(train_perplexity)

    print("done in %0.3fs." % (time() - t0))

    df = pd.DataFrame(grid)
    df.to_csv('sklearn_perplexity.csv')
    print(df)
    plt.figure(figsize=(14, 8), dpi=120)
    # plt.subplot(221)
    plt.plot(df.columns.values, df.iloc[0].values, '#007A99')
    plt.xticks(df.columns.values)
    plt.xlabel('topic number')
    plt.ylabel('train Perplexity')
    plt.title('主题数和困惑度的关系')
    plt.savefig('lda_topic_perplexity.png', bbox_inches='tight', pad_inches=0.1)
    plt.show()


if __name__ == '__main__':
    food_news_corpus = get_corpus('corpus/news_content_corpus.txt')
    topic_analyze(food_news_corpus)
