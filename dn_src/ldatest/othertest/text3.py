#coding=utf-8
def test1():
    pagenum = "共1285条/26页".split('/')[1][:-3]

    print (pagenum)
    import pkuseg

    seg = pkuseg.pkuseg()  # 以默认配置加载模型
    text = seg.cut('我爱北京天安门')  # 进行分词
    print(text)
    # str2 = open('./doc_shipin4.txt', 'r', encoding='UTF-8').read()
    # print (type(str2))
    "topic0_doc10133.txt".split('_')[1]

def splitword():
    import csv
    with open('E:\\pySpace\\MachineLearning\\ldatest\\csv\\testcsv\shipintopic.csv', 'r',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            topic = row['topic'].split()[:3]
            print (topic)
            keyword=""
            for i in range(len(topic)):
                keyword=keyword+'\r'+topic[i]
        print(keyword)

def agrmax():
    import numpy as np
    a = np.array([[1, 5, 5, 2],
                  [9, 6, 2, 8],
                  [3, 7, 9, 1]])
    print(np.argmax(a, axis=1))
if __name__=="__main__":
    agrmax()