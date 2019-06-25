#-*- coding:utf-8-*-
from gensim import corpora,models
from gensim.corpora import Dictionary
from gensim.models import LdaModel

def readtxt(filepath):
    corpus = []
    with open(filepath,'r', encoding='UTF-8') as f:
        for line in f.readlines():
            linewords=line.split()
            for word in linewords:
                corpus.append([word])
    return corpus
def createcorpus():
    corpustext = readtxt('../corpus/doc_shipin.txt')
    # id2word = corpora.Dictionary.load_from_text(corpus)
    # mm = corpora.MmCorpus('doc_shipin.mm')
    dictionary = Dictionary(corpustext)
    corpus = [dictionary.doc2bow(text) for text in corpustext]
    # 模型训练
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=106)

    # lda.get_topics()

    # 打印前20个topic的词分布
    print(lda.print_topics(10, 10))
    lda.save('../corpus/shipin.model')
    #提取每篇文档所属主题
    for i in lda.get_document_topics(corpus)[:]:
        listj=[]
        for j in i:
            listj.append(j[1])
        bz=listj.index(max(listj))
        print(i[bz][0])

if __name__=='__main__':
    # 语料导入
    # 模型的保存和加载
    createcorpus()

    #对新文档预测
    testdoc=[]
    with open('../txt/topic_doc_pk/topic0/topic0_doc978.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            linewords = line.split()
            for word in linewords:
                testdoc.append(word)
    corpustext = readtxt('../corpus/doc_shipin.txt')
    dictionary = Dictionary(corpustext)
    lda = models.ldamodel.LdaModel.load('../corpus/shipin.model')
    doc_bow = dictionary.doc2bow(testdoc)
    doc_lda = lda[doc_bow]
    print(doc_lda)
    for topic in doc_lda:
        print("%s\t%f\n" % (lda.print_topic(topic[0]) ,topic[1]))
