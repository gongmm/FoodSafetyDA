# -*- coding: utf-8 -*-
import csv
import os
import pandas as pd


def gbk_2_utf(readfile, writefile):
    """ 读取gbk格式的文件转码为utf-8格式"""
    writefile = open(writefile, 'w', encoding='utf-8')
    with open(readfile, 'r', encoding="GB18030") as f:
        for row in f:
            row = row.encode("utf-8").decode("utf-8")
            writefile.write(row)


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
    topic_news_number = []
    # 读写csv文件
    df = pd.read_csv("data/all_news_data_topic_format.csv")
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
    topic_post_number = []
    topic_read_number = []
    topic_reply_number = []
    # 读写csv文件
    df = pd.read_csv("data/forum_topic" + str(topic_id) + "_format.csv")
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
    topic_post_number = []
    topic_comment_number = []
    topic_like_number = []
    topic_repost_number = []
    # 读写csv文件
    df = pd.read_csv("data/weibo_topic" + str(topic_id) + "_format.csv")
    df['pub_date'] = pd.to_datetime(df['pub_date'])
    df = df.set_index('pub_date')
    for month in range(1, 13):
        date_str = '2018-' + str(month)
        # 得到某月数据
        df_month = df[date_str]
        topic_post_number.append(df_month.shape[0])
        topic_comment_number.append(df_month['comment_num'].sum())
        topic_like_number.append(df_month['like_num'].sum())
        topic_repost_number.append(df_month['repost_num'].sum())
    return topic_post_number, topic_comment_number, topic_like_number, topic_repost_number


def calculate_fever(readfile='data/sentiment_topic_analysis_info.csv'):
    with open(readfile, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)


if __name__ == '__main__':
    # gbk_2_utf('data/forum_topic21.csv', 'data/forum_topic21_format.csv')
    # reformat_date("data/all_news_data_utf_topic.csv", "data/all_news_data_topic_format.csv")
    topic_num = 21
    get_forum_info_by_topic(topic_id=21)
    # calculate()
