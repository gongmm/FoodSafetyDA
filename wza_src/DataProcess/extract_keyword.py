from jieba.analyse import *
import os


def get_all_files(path):
    """
    获得路径下的所有文件，包括子文件夹下的文件

    Args:
        path :  目标文件夹的路径
    """
    files_ = []
    dir_list = os.listdir(path)
    for i in range(0, len(dir_list)):
        path = os.path.join(path, dir_list[i])
        if os.path.isdir(path):
            files_.extend(get_all_files(path))
        if os.path.isfile(path):
            files_.append(path)
    return files_


def extract_single_doc(content):
    """
    提取文本中的前十个关键词

    Args:
        content: 文本内容

    Returns:
        前十个关键词 list

    """
    keywords = []
    # for keyword, weight in extract_tags(content, withWeight=True):
    #     keywords.append(keyword)
    #     print('%s %s' % (keyword, weight))
    for keyword, weight in textrank(content, withWeight=True):
        #     print('%s %s' % (keyword, weight))
        keywords.append(keyword)
    return keywords[:10]


def extract_event(path):
    """
    提取一个事件中的关键词，将描述该事件的文档拼接然后进行关键词提取
    Args:
        path: 事件文件夹所在的路径

    Returns:
        事件的前十个关键词

    """
    content = ''
    files = get_all_files(path)
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content += f.read()
    print(path)
    return extract_single_doc(content)


def extract_topic(path):
    """
    提取话题中所有事件的关键词
    Args:
        path: 话题文件夹所在的路径

    Returns:

    """
    topic_keywords = []
    events_path = os.path.join(path, 'events')
    events = os.listdir(events_path)
    for event in events:
        keywords = extract_event(os.path.join(events_path, event))
        topic_keywords.append(keywords)
    save_keywords(path, topic_keywords)


def save_keywords(path, topic_keywords):
    """
    保存话题中各个事件的关键词
    Args:
        path: 话题文件夹所在的路径
        topic_keywords: 话题中各个事件的关键词列表

    Returns:

    """
    events_keyword_dir = 'events_keyword'
    save_path = os.path.join(path, events_keyword_dir)
    # 如果不存在则创建目录
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for index in range(len(topic_keywords)):
        filename = 'event' + str(index) + '.txt'
        file_path = os.path.join(save_path, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(' '.join(topic_keywords[index]))


if __name__ == '__main__':
    data_path = 'topic_doc'
    topic_num = 2
    for index in range(topic_num):
        topic_path = os.path.join(data_path, 'topic' + str(index))
        extract_topic(topic_path)
