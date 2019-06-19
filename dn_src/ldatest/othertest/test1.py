def splitword():
    import csv
    with open('D:\\pySpace\\MachineLearning\\ldatest\\csv\\testcsv\shipintopic.csv', 'r',encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        i=0
        for row in reader:
            topic = row['topic'].split()[:3]
            #topicid=row['topicid']
            i+=1
            print (len(topic))
            # keyword=""
            # for i in range(len(topic)):
            #     keyword=keyword+' '+topic[i]
            #     print(keyword)
        print (i)
if __name__=="__main__":
    splitword()