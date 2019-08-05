import os
import pandas as pd
import re

base_dir = 'topic_doc'
result_dir = 'result'
topic_words_csv = os.path.join(result_dir, 'food_topic_word.csv')


def sort_key(s):
    if s:
        try:
            c = re.findall('\\d+', s)[0]
        except:
            c = -1
        return int(c)


def get_topic_words(topic):
    """根据主题文件夹名读取csv文件获得主题下的词

    Args:
        topic: 字符串，“topic1”之类的

    Returns:
        topic_word: 字符串，主题下的词
    """
    topic_id = int(topic[5:])  # 从“topic1”中获得数字
    df = pd.read_csv(topic_words_csv)
    topic_word = df.loc[topic_id, 'topic_word']
    return topic_word


def get_file_list(parent_dir, sub_dir):
    """获得子文件夹路径及子文件夹下所有文件名

    Args:
        parent_dir: 字符串，父文件夹名称
        sub_dir: 字符串，子文件夹名称

    Returns:
        dir: 字符串，子文件夹路径
        file_list: 列表，子文件夹下所有文件名

    """
    dir = os.path.join(base_dir, parent_dir, sub_dir)
    file_list = os.listdir(dir)
    file_list.sort(key=sort_key)
    return dir, file_list


def event2csv():
    """将所有主题的事件信息存入csv文件中"""
    topic_list = os.listdir(base_dir)
    topic_list.sort(key=sort_key)
    total_data = []
    for topic in topic_list:
        print('--------%s--------' % topic)
        topic_words = get_topic_words(topic)
        event_dir, event_list = get_file_list(topic, 'events')
        event_keyword_dir, event_keyword_list = get_file_list(topic, 'events_keyword')

        event_num = len(event_list)

        for i in range(len(event_list)):
            event_path = os.path.join(event_dir, event_list[i])
            doc_num = len(os.listdir(event_path))

            keyword_path = os.path.join(event_keyword_dir, event_keyword_list[i])
            with open(keyword_path, 'r', encoding='utf-8') as f:
                content = f.read()

            total_data.append((topic, topic_words, event_num, i, doc_num, content))

    # 写入csv
    event_csv = os.path.join(result_dir, 'topic_events.csv')
    pd_df = pd.DataFrame(total_data, columns=['topic_id', 'topic_words', 'event_num', 'event_id', 'doc_num', 'event_keywords'])
    pd_df.to_csv(event_csv, index=False)


if __name__ == '__main__':
    event2csv()