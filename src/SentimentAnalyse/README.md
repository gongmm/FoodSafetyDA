# 舆情分析

* 话题热度计算
* GPR趋势预测
* 月份话题热度排行榜

## 依赖 ##

* scikit-learn==0.21.2
* pandas==0.22.0
* pyecharts==1.3.1

## 运行

### 文件夹说明 ###

* `chart`：存放话题热度排行榜图表
* `origin_data`：存放爬取到的微博原始数据
* `format_data`：存放格式化后的数据

### 文件说明 ###

* `data_format.py`：数据格式化

  * 获取文件编码类型
  * 读取gbk格式的文件转码为utf-8格式
  * 格式化文件中的日期格式
  * 文件格式化：转码、格式化日期

  ```shell
  $ python data_format.py
  ```

  * 将原始文件放置在`origin_data`中，格式化后的数据将放置在`format_data`中

* `sentiment_fever.py`：话题热度计算

  ```shell
  $ python sentiment_fever.py
  ```

  * 绘制各个话题的2018年的热度变化图

* `sentiment_fever_day.py`：话题热度变化(天)

  ```shell
  $ python sentiment_fever_day.py
  ```

  * 绘制各个话题各个月的热度变化图

* `gpr_trend_prediction.py`：高斯过程回归进行趋势预测

  ```shell
  $ python gpr_trend_prediction.py
  ```

  * 绘制预测结果

* `gray_forcast.py`：热度灰色预测

  ```shell
  $ python gray_forcast.py
  ```

* `fever_rank`：得到某月的话题热度排行榜

  ```shell
  $ python fever_rank.py
  ```

* `state_transition.py`、`trend_predict.py`：基于马尔可夫链的趋势预测（仅作尝试，结果不理想）

## 结果

- 话题热度计算
- 话题趋势预测
- 8月份话题热度排行榜

