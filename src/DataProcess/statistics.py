import os
import matplotlib.pyplot as plt

base_dir = 'topic_doc'
statistics_dir = 'statistics'
if not os.path.exists(statistics_dir):
    os.makedirs(statistics_dir)
event_doc_dir = os.path.join(statistics_dir, 'event_doc_count')
if not os.path.exists(event_doc_dir):
    os.makedirs(event_doc_dir)


def count_topic_doc():
    topic_dir_list = os.listdir(base_dir)
    topic_doc_num = []
    for topic_dir in topic_dir_list:
        topic_path = os.path.join(base_dir, topic_dir)
        doc_list = [f for f in os.listdir(topic_path) if f.endswith('.txt')]
        topic_doc_num.append(len(doc_list))
    topic_num = len(topic_dir_list)
    file = os.path.join(statistics_dir, 'topic_doc_num.png')
    x = [i for i in range(topic_num)]
    plt.clf()  # 先清空当前图形，防止画多了
    plt.plot(x, topic_doc_num)
    plt.xlabel('topic id')
    plt.ylabel('document number')
    plt.title('topic-document distribution')
    plt.savefig(file)


def count_topic_event():
    topic_dir_list = os.listdir(base_dir)
    topic_event_num = []
    for topic_dir in topic_dir_list:
        event_path = os.path.join(base_dir, topic_dir, 'events')
        event_num = len(os.listdir(event_path))
        topic_event_num.append(event_num)
    topic_num = len(topic_dir_list)
    file = os.path.join(statistics_dir, 'topic_event_num.png')
    x = [i for i in range(topic_num)]
    plt.clf()  # 先清空当前图形，防止画多了
    plt.plot(x, topic_event_num)
    plt.xlabel('topic id')
    plt.ylabel('event number')
    plt.title('topic-event distribution')
    plt.savefig(file)


def count_event_doc():
    topic_dir_list = os.listdir(base_dir)
    for topic_dir in topic_dir_list:
        event_dir_path = os.path.join(base_dir, topic_dir, 'events')
        event_dir_list = os.listdir(event_dir_path)
        event_doc_num = []
        for event_dir in event_dir_list:
            event_path = os.path.join(event_dir_path, event_dir)
            doc_num = len(os.listdir(event_path))
            event_doc_num.append(doc_num)
        event_num = len(event_dir_list)
        file = os.path.join(event_doc_dir, topic_dir + '_events_doc_num.png')
        x = [i for i in range(event_num)]
        plt.clf()  # 先清空当前图形，防止画多了
        plt.plot(x, event_doc_num)
        plt.xlabel('event id')
        plt.ylabel('document number')
        plt.title(topic_dir + "'s event-document distribution")
        plt.savefig(file)


if __name__ == '__main__':
    count_topic_doc()
    count_topic_event()
    count_event_doc()
