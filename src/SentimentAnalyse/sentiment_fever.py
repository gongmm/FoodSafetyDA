# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

origin_path = 'origin_data'
format_path = 'format_data'


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


def get_id_list():
    id_list = []
    with open('keywords.txt', 'r') as f:
        for info in f.readlines():
            topic_id = info.split(',')[0]
            id_list.append(topic_id)
    return id_list


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
    try:
        df = pd.read_csv(file_path)
    except:
        print("论坛信息中不存在topic_" + str(topic_id))
        topic_post_number = [0] * 12
        topic_reply_number = [0] * 12
        topic_read_number = [0] * 12
    else:
        df['pub_date'] = pd.to_datetime(df['pub_date'])
        df = df.set_index('pub_date')
        for month in range(1, 13):
            if month >= 10:
                date_str = '2018-' + str(month)
            else:
                date_str = '2018-0' + str(month)
            # 得到某月数据
            try:
                df_month = df[date_str]
            except:
                print(file_path)
            else:
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

    try:
        # 读写csv文件
        df = pd.read_csv(file_path)
    except:
        print("微博信息中不存在topic_" + str(topic_id))
        topic_post_number = [0] * 12
        topic_comment_number = [0] * 12
        topic_like_number = [0] * 12
        topic_repost_number = [0] * 12
    else:
        df['pub_date'] = pd.to_datetime(df['pub_date'])
        df = df.set_index('pub_date')
        for month in range(1, 13):
            if month >= 10:
                date_str = '2018-' + str(month)
            else:
                date_str = '2018-0' + str(month)
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


def calculate_fever_by_topic(topic_id, standardize=True, readfile='format_data/sentiment_topic_analysis_info.csv'):
    w1 = 0.65
    w2 = 0.3
    w3 = 0.05
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
    result_weibo = calculate_core(weibo_post_number, weibo_post_w) + calculate_core(weibo_comment_number,
                                                                                    weibo_comment_w) \
                   + calculate_core(weibo_like_number, weibo_like_w) + calculate_core(weibo_repost_number,
                                                                                      weibo_repost_w)

    result = (result_news + result_forum + result_weibo).tolist()
    if standardize:
        result = standardization(result)
    result = round_result(result)
    return result


def calculate_three_part_by_topic(topic_id):
    w1 = 0.5
    w2 = 0.25
    w3 = 0.25
    post_w = 0.8
    reply_w = 0.15
    read_w = 0.05

    weibo_post_w = 0.4
    weibo_comment_w = 0.3
    weibo_like_w = 0.1
    weibo_repost_w = 0.2

    news_number = get_news_number_by_topic(topic_id)
    forum_post_number, forum_reply_number, forum_read_number = get_forum_info_by_topic(topic_id)
    weibo_post_number, weibo_comment_number, weibo_like_number, weibo_repost_number = get_weibo_info_by_topic(topic_id)

    result_news = calculate_core(news_number, w1)
    result_forum = calculate_core(forum_post_number, post_w) + calculate_core(forum_read_number, read_w) \
                   + calculate_core(forum_reply_number, reply_w)
    result_weibo = calculate_core(weibo_post_number, weibo_post_w) + calculate_core(weibo_comment_number,
                                                                                    weibo_comment_w) \
                   + calculate_core(weibo_like_number, weibo_like_w) + calculate_core(weibo_repost_number,
                                                                                      weibo_repost_w)

    result_news = result_news.tolist()
    result_forum = result_forum.tolist()
    result_weibo = result_weibo.tolist()

    return result_news, result_forum, result_weibo


def calculate_three_part_by_month(month, topic_number=45, standardize=True):
    w1 = 0.5
    w2 = 0.15
    w3 = 0.35
    post_w = 0.8
    reply_w = 0.15
    read_w = 0.05

    weibo_post_w = 0.4
    weibo_comment_w = 0.3
    weibo_like_w = 0.1
    weibo_repost_w = 0.2

    result_news = []
    result_forum = []
    result_weibo = []

    id_list = get_id_list()
    for topic_id in range(topic_number):
        if str(topic_id) in id_list:
            news = get_news_number_by_topic(topic_id)
            forum_post_number, forum_reply_number, forum_read_number = get_forum_info_by_topic(topic_id)
            weibo_post_number, weibo_comment_number, weibo_like_number, weibo_repost_number = get_weibo_info_by_topic(
                topic_id)
            forum = calculate_core(forum_post_number, post_w) + calculate_core(forum_read_number, read_w) \
                    + calculate_core(forum_reply_number, reply_w)
            weibo = calculate_core(weibo_post_number, weibo_post_w) + calculate_core(weibo_comment_number,
                                                                                     weibo_comment_w) \
                    + calculate_core(weibo_like_number, weibo_like_w) + calculate_core(weibo_repost_number,
                                                                                       weibo_repost_w)
            result_news.append(news[month - 1])
            result_forum.append(forum[month - 1])
            result_weibo.append(weibo[month - 1])

    if standardize:
        standardization(result_news)
        standardization(result_forum)
        standardization(result_weibo)

    result_news = calculate_core(result_news, w1)
    result_forum = calculate_core(result_forum, w2)
    result_weibo = calculate_core(result_weibo, w3)

    result_fever = (result_news + result_forum + result_weibo).tolist()
    result_news = result_news.tolist()
    result_forum = result_forum.tolist()
    result_weibo = result_weibo.tolist()

    return result_fever, result_news, result_forum, result_weibo


def round_result(result_list):
    for index in range(len(result_list)):
        result_list[index] = round(result_list[index])
    return result_list


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
        if max_value - min_value == 0:
            fever_list[index] = 0
        else:
            fever_list[index] = (fever_list[index] - min_value) / (max_value - min_value)
    return fever_list


def calculate_news_number():
    number = 0
    for topic_id in range(45):
        file_path = os.path.join(format_path, "weibo_topic" + str(topic_id) + ".csv")
        try:
            # 读写csv文件
            df = pd.read_csv(file_path)
        except:
            print("微博信息中不存在topic_" + str(topic_id))
        else:
            number += df.shape[0]
    return number


if __name__ == '__main__':
    # format_data()
    print(calculate_news_number())
    # gbk_2_utf('format_data/forum_topic21.csv', 'format_data/forum_topic21_format.csv')
    # reformat_date("format_data/all_news_data_utf_topic.csv", "format_data/all_news_data_utf_topic.csv")
    topic_num = 21
    draw_fever_trend(topic_id=topic_num)
