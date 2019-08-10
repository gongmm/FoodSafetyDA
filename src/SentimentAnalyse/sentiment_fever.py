# -*- coding: utf-8 -*-
import csv
import os
import pandas as pd
import numpy as np
import chardet
from matplotlib import pyplot as plt

origin_path = 'origin_data'
format_path = 'format_data'


# 获取文件编码类型
def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        data = f.read()
        return chardet.detect(data)['encoding']


def gbk_2_utf(readfile, tmp_file='tmp'):
    """ 读取gbk格式的文件转码为utf-8格式"""
    tmp_file = os.path.join(origin_path, tmp_file)
    try:
        with open(readfile, 'r', encoding="GB18030") as f:
            with open(tmp_file, 'w', encoding='utf-8') as f_w:
                for row in f:
                    row = row.encode("utf-8").decode("utf-8")
                    f_w.write(row)
    except Exception as e:
        print(e)
        os.remove(tmp_file)
    else:
        os.remove(readfile)
        os.rename(tmp_file, readfile)


def reformat_date(readfile, writefile):
    # 读csv文件
    df = pd.read_csv(readfile)
    for i in range(df['pub_date'].shape[0]):
        # for row in df['pub_date']:
        df.loc[i, 'pub_date'] = df.loc[i, 'pub_date'].replace('年', '/')
        df.loc[i, 'pub_date'] = df.loc[i, 'pub_date'].replace('月', '/')
        df.loc[i, 'pub_date'] = df.loc[i, 'pub_date'].replace('日', '')
    df['pub_date'] = pd.to_datetime(df['pub_date'])  # 将数据类型转换为日期类型
    df.to_csv(writefile)


def get_news_number_by_topic(topic_id):
    file_path = os.path.join(format_path, 'all_news_data_utf_topic.csv')
    topic_news_number = []
    # 读写csv文件
    df = pd.read_csv(file_path)
    # 筛选主题数据
    df = df[(df['topic_id'] == topic_id)]
    df['pub_date'] = pd.to_datetime(df['pub_date'])
    # 得到某月数据
    df = df.set_index('pub_date')
    for month in range(1, 13):
        date_str = '2018-' + str(month)
        topic_news_number.append(df[date_str].shape[0])

    return topic_news_number


def get_news_number():
    news_number = []
    for topic_id in range(0, 45):
        news_number.append(get_news_number_by_topic(topic_id))
    return news_number


def get_forum_info_by_topic(topic_id):
    file_path = os.path.join(format_path, "forum_topic" + str(topic_id) + ".csv")
    topic_post_number = []
    topic_read_number = []
    topic_reply_number = []
    # 读写csv文件
    df = pd.read_csv(file_path)
    df['pub_date'] = pd.to_datetime(df['pub_date'])
    df = df.set_index('pub_date')
    for month in range(1, 13):
        date_str = '2018-' + str(month)
        # 得到某月数据
        df_month = df[date_str]
        topic_post_number.append(df_month.shape[0])
        topic_reply_number.append(df_month['reply_num'].sum())
        topic_read_number.append(df_month['read_num'].sum())
    return topic_post_number, topic_reply_number, topic_read_number


def get_weibo_info_by_topic(topic_id):
    file_path = os.path.join(format_path, "weibo_topic" + str(topic_id) + ".csv")
    topic_post_number = []
    topic_comment_number = []
    topic_like_number = []
    topic_repost_number = []
    # 读写csv文件
    df = pd.read_csv(file_path)
    df['pub_date'] = pd.to_datetime(df['pub_date'])
    df = df.set_index('pub_date')
    for month in range(1, 13):
        date_str = '2018-' + str(month)
        # 得到某月数据
        df_month = df[date_str]
        topic_post_number.append(df_month.shape[0])
        topic_comment_number.append(df_month['comment'].sum())
        topic_like_number.append(df_month['like'].sum())
        topic_repost_number.append(df_month['repost'].sum())
    return topic_post_number, topic_comment_number, topic_like_number, topic_repost_number


def calculate_core(number_list, w):
    array = np.array(number_list)
    array = np.dot(w, array)
    return array


def calculate_fever_by_topic(topic_id, readfile='format_data/sentiment_topic_analysis_info.csv'):
    w1 = 0.5
    w2 = 0.3
    w3 = 0.2
    post_w = 0.8 * w2
    reply_w = 0.15 * w2
    read_w = 0.05 * w2

    weibo_post_w = 0.4 * w3
    weibo_comment_w = 0.3 * w3
    weibo_like_w = 0.1 * w3
    weibo_repost_w = 0.2 * w3

    news_number = get_news_number_by_topic(topic_id)
    forum_post_number, forum_reply_number, forum_read_number = get_forum_info_by_topic(topic_id)
    weibo_post_number, weibo_comment_number, weibo_like_number, weibo_repost_number = get_weibo_info_by_topic(topic_id)

    result_news = calculate_core(news_number, w1)
    result_forum = calculate_core(forum_post_number, post_w) + calculate_core(forum_read_number, read_w) \
                   + calculate_core(forum_reply_number, reply_w)
    result_weibo = calculate_core(weibo_post_number, weibo_post_w) + calculate_core(weibo_comment_number, weibo_comment_w) \
                   + calculate_core(weibo_like_number, weibo_like_w) + calculate_core(weibo_repost_number, weibo_repost_w)

    result = (result_news + result_forum + result_weibo).tolist()
    result = standardization(result)
    return result


def format_data():
    files = os.listdir(origin_path)
    # 进行转码
    for file in files:
        file_path = os.path.join(origin_path, file)
        result_path = os.path.join(format_path, file)
        gbk_2_utf(file_path)
        reformat_date(file_path, result_path)


def draw_fever_trend(topic_id):
    fever_list = calculate_fever_by_topic(topic_id)
    x = [i for i in range(1, 13)]
    # 绘制折线图，设置线宽
    plt.plot(x, fever_list, linewidth=2)

    # 设置图表标题，并给坐标轴加上标签
    plt.title("sentiment fever by month", fontsize=24)
    plt.xlabel("month", fontsize=14)
    plt.ylabel("fever", fontsize=14)
    # 设置刻度标记的大小
    plt.xticks([i for i in range(1, 13)])
    plt.tick_params(axis='both', labelsize=14)

    plt.show()


def standardization(fever_list):
    max_value = max(fever_list)
    min_value = min(fever_list)
    for index in range(len(fever_list)):
        fever_list[index] = (fever_list[index] - min_value) / (max_value - min_value)
    return fever_list


if __name__ == '__main__':
    # format_data()
    # gbk_2_utf('format_data/forum_topic21.csv', 'format_data/forum_topic21_format.csv')
    # reformat_date("format_data/all_news_data_utf_topic.csv", "format_data/all_news_data_utf_topic.csv")
    topic_num = 21
    # calculate_fever_by_topic(topic_id=21)
    draw_fever_trend(topic_id=21)
    # calculate()
