from os import listdir
from gensim.models import Word2Vec
from gensim.models.word2vec import PathLineSentences
import multiprocessing
import os
import gensim
import pymysql
def train():
    """训练 并保存Doc2Vec 模型
    """

    # 先把所有文档的路径存进一个 array中，docLabels：
    input_dir = "../txt/topic_doc_pk"
    # 训练 Doc2Vec，并保存模型：
    gensim.models
    model=Word2Vec(PathLineSentences(input_dir),size=256,window=10,min_count=5,workers=multiprocessing.cpu_count(),iter=10)
    outp1="../word2vec_models/shipin.model"
    outp2="../word2vec_models/shipin.txt"
    model.save(outp1)
    model.similarity()
    model.wv.save_word2vec_format(outp2,binary=False)
    print("model saved")
import logging
logger = logging.getLogger(__name__)
MAX_WORDS_IN_BATCH = 10000
from gensim import utils, matutils  # utility fnc for pickling, common scipy operations etc
import itertools

class PathLineSentences(object):

    def __init__(self, source, max_sentence_length=MAX_WORDS_IN_BATCH, limit=None):
        """
        Parameters
        ----------
        source : str
            Path to the directory.
        limit : int or None
            Read only the first `limit` lines from each file. Read all if limit is None (the default).

        """
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
            self.input_files=[]
            for fpathe,dirs,fs in os.walk(self.source):
                for f in fs:
                    self.input_files.append(os.path.join(fpathe,f))
            self.input_files.sort()  # makes sure it happens in filename order
        else:  # not a file or a directory, then we can't do anything with it
            raise ValueError('input is neither a file nor a path')
        logger.info('files read into PathLineSentences:%s', '\n'.join(self.input_files))

    def __iter__(self):
        """iterate through the files"""
        for file_name in self.input_files:
            logger.info('reading file %s', file_name)
            with utils.smart_open(file_name) as fin:
                for line in itertools.islice(fin, self.limit):
                    line = utils.to_unicode(line).split()
                    i = 0
                    while i < len(line):
                        yield line[i:i + self.max_sentence_length]
                        i += self.max_sentence_length

def usemodel():
    model = gensim.models.KeyedVectors.load_word2vec_format('../corpus/sgns.renmin.word',binary=False)
    print(model.get_vector('十分愤怒'))
    sim= model.most_similar(u'瘦肉精',topn=10)
    print('\n瘦肉精-top10:')
    for item in sim:
        print(item[0],item[1])
    sim2 = model.most_similar(u'地沟油', topn=10)
    print('\n地沟油-top10:')
    for item in sim2:
        print(item[0], item[1])
    sim3 = model.most_similar(u'非洲猪瘟', topn=10)
    print('\n非洲猪瘟-top10:')
    for item in sim3:
        print(item[0], item[1])




if __name__=='__main__':
    usemodel()