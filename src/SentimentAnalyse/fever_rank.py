from sentiment_fever import calculate_fever_by_topic


def get_keywords(id):
    id_list = []
    word_list = []
    with open('keywords.txt', 'r') as f:
        for info in f.readlines():
            topic_id = info.split(',')[0]
            topic_word = info.split(',')[-1].strip()
            id_list.append(topic_id)
            word_list.append(topic_word)
    index = id_list.index(str(id))
    keyword = word_list[index]
    return keyword


def get_id_list():
    id_list = []
    with open('keywords.txt', 'r') as f:
        for info in f.readlines():
            topic_id = info.split(',')[0]
            id_list.append(topic_id)
    return id_list


def topic_fever_rank(month, topic_num=45):
    topic_fever_dict = {}
    id_list = get_id_list()
    for topic in range(topic_num):
        if str(topic) in id_list:
            fever_list = calculate_fever_by_topic(topic_id=topic, standardize=False)
            fever = fever_list[month - 1]
            keyword = get_keywords(topic)
            topic_fever_dict[keyword] = fever
    z = zip(topic_fever_dict.values(), topic_fever_dict.keys())
    result = sorted(z, reverse=True)
    result = [t[-1] for t in result]
    return result


if __name__ == '__main__':
    cur_month = 8
    topic_fever_rank(cur_month)
