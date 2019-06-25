import os
def test1():
    filepath='E:\\foodtag\\652-1000\\'
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        child0=allDir.split('.')[0]
        print (child0)
        with open("E:\\foodtag\\foodTagTxtlast\\" + child0 + '.txt', 'w', encoding='utf-8') as fw:
            with open(child,'r',encoding='utf-8') as fr:
                anns=fr.readlines()
                print (anns)
                flag = True
                index=0
                i=1
                for line in anns:
                    if (line =="\n" or line.split()[0]=="O" ) and flag:
                        fw.write("\n")
                        flag = False
                    elif (line =="\n" or line.split()[0]=="O" ) and flag==False:
                        continue
                    else:
                        if line.split()[0]=="B-Food":
                            i=0
                            continue
                        if line.split()[0]=="I-Food":
                            continue
                        if i==0:
                            fw.write(line.split()[0]+" "+"B-Food")
                            flag=True
                            i=i+1
                        else:
                            fw.write(line)

def test2():
    filepath = 'E:\\foodtag\\foodTagTxtlast\\'
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        child0 = allDir.split('.')[0]
        import re
        childnum = re.findall('\d+', child0)
        num=int(childnum[0])
        if num<500:
            with open('food.train', 'a+', encoding='utf-8') as fw:
                with open(child, 'r', encoding='utf-8') as fr:
                        anns = fr.read()
                fw.write(anns)
        elif 500<=num<750:
            with open('food.test', 'a+', encoding='utf-8') as fw:
                with open(child, 'r', encoding='utf-8') as fr:
                        anns = fr.read()
                fw.write(anns)
        elif num>700:
            with open('food.dev', 'a+', encoding='utf-8') as fw:
                with open(child, 'r', encoding='utf-8') as fr:
                        anns = fr.read()
                fw.write(anns)
def test3():
    filepath = 'E:\\foodtag\\652-1000txt\\'
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        child0 = allDir.split('.')[0]
        print(child0)
        with open("E:\\foodtag\\FoodTagNew\\" + child0 + '.txt', 'w', encoding='utf-8') as fw:
            with open(child, 'r', encoding='utf-8') as fr:
                anns = fr.readlines()
                print(anns)
                flag = True
                index = 0
                for line in anns:
                    if index==0:
                        index += 1
                        continue
                    else:
                        fw.write(line)
                        index += 1


if __name__=='__main__':
    test2()