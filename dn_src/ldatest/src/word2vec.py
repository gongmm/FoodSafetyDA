from os import listdir

import multiprocessing
import os
import gensim
from gensim import utils  # utility fnc for pickling, common scipy operations etc
from gensim.models.word2vec import Word2Vec
from gensim.models.word2vec import PathLineSentences
import itertools
import logging

"""
训练 并保存Doc2Vec 模型
得到 词向量
"""


def train():
    # 先把所有文档的路径存进一个 array中，docLabels：
    input_dir = "../txt/topic_doc_pk"
    # 训练 Doc2Vec，并保存模型：
    # 特征向量维度：256；窗口大小：5；训练并行数；迭代次数
    model = Word2Vec(PathLineSentences(input_dir), size=256, window=10, min_count=5,
                     workers=multiprocessing.cpu_count(), iter=10)
    output_model = "../word2vec_models/food_word_vector.model"
    output_txt = "../word2vec_models/good_word_vector.txt"
    model.save(output_model)
    model.wv.save_word2vec_format(output_txt, binary=False)
    print("model saved")
    # model.similarity(u'瘦肉精', u'地沟油')


logger = logging.getLogger(
    __name__)
MAX_WORDS_IN_BATCH = 10000

"""
sentence迭代器
返回sentence的一个word（utf8格式）的列表
"""


class PathLineSentences(object):
    """
        Parameters
        ----------
        source : str
            Path to the directory.
        limit : int or None
            Read only the first `limit` lines from each file. Read all if limit is None (the default).

    """

    def __init__(self, source, max_sentence_length=MAX_WORDS_IN_BATCH, limit=None):

        self.source = source
        self.max_sentence_length = max_sentence_length
        self.limit = limit

        if os.path.isfile(self.source):
            logger.debug('single file given as source, rather than a directory of files')
            logger.debug('consider using models.word2vec.LineSentence for a single file')
            self.input_files = [self.source]  # force code compatibility with list of files
        elif os.path.isdir(self.source):
            self.source = os.path.join(self.source, '')  # ensures os-specific slash at end of path
            logger.info('reading directory %s', self.source)
            # 存储目录下的所有文件（排序）
            self.input_files = []
            # 提取目录下的所有文件
            for root, dirs, files in os.walk(self.source):
                for f in files:
                    self.input_files.append(os.path.join(root, f))
            self.input_files.sort()  # makes sure it happens in filename order
        else:  # not a file or a directory, then we can't do anything with it
            raise ValueError('input is neither a file nor a path')
        logger.info('files read into PathLineSentences:%s', '\n'.join(self.input_files))

    """iterate through the files"""

    def __iter__(self):

        for file_name in self.input_files:
            logger.info('reading file %s', file_name)
            with utils.smart_open(file_name) as fin:
                # 获得文件中的一行
                for line in itertools.islice(fin, self.limit):
                    # 将一行内容（分词结果）以空格切分为链表
                    line = str(line, encoding='utf-8').split()
                    i = 0
                    while i < len(line):
                        # 分次返回指定长度的句子的分词列表
                        yield line[i:i + self.max_sentence_length]
                        i += self.max_sentence_length


def use_model():
    model = gensim.models.KeyedVectors.load_word2vec_format('../corpus/sgns.renmin.word', binary=False)
    print(model.get_vector('瘦肉精'))
    sim = model.most_similar(u'瘦肉精', topn=10)
    print('\n瘦肉精-top10:')
    for item in sim:
        print(item[0], item[1])
    sim2 = model.most_similar(u'地沟油', topn=10)
    print('\n地沟油-top10:')
    for item in sim2:
        print(item[0], item[1])
    sim3 = model.most_similar(u'猪瘟', topn=10)
    print('\n非洲猪瘟-top10:')
    for item in sim3:
        print(item[0], item[1])


if __name__ == '__main__':
    # train()
    use_model()