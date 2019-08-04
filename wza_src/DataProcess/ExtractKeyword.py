from jieba.analyse import *
import os


def get_all_files(path):
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
    keywords = []
    # for keyword, weight in extract_tags(content, withWeight=True):
    #     keywords.append(keyword)
    #     print('%s %s' % (keyword, weight))
    for keyword, weight in textrank(content, withWeight=True):
        #     print('%s %s' % (keyword, weight))
        keywords.append(keyword)
    return keywords[:10]


def extract_event(path):
    content = ''
    files = get_all_files(path)
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content += f.read()
    print(path)
    return extract_single_doc(content)


def extract_topic(path):
    topic_keywords = []
    events_path = os.path.join(path, 'events')
    events = os.listdir(events_path)
    for event in events:
        keywords = extract_event(os.path.join(events_path, event))
        topic_keywords.append(keywords)
    save_keywords(path, topic_keywords)


def save_keywords(path, topic_keywords):
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
