# 对标记好的新闻数据进行切分

* 按照7：2：1的比例划分训练集、测试集、开发集
* 对长文本按照标点符号和句子长度进行切分
* 划分好的训练集、测试集、开发集将放置在origin_data中
* 切分好的数据将放置在data文件夹中

## 依赖

- anns_data：存放标记好的新闻数据


## 运行

将标记好的文本放置在anns_data文件夹下

```shell
$ python main.py
```

## 结果

- 得到切分好的数据集，可直接放入BiLSTM-CRF模型中进行训练

