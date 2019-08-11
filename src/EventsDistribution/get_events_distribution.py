import os
import re
import cpca

base_dir = os.path.join('..', 'DataProcess', 'topic_doc')

# 搜索省份的网址
seach_url = 'http://xzqh.mca.gov.cn/fuzzySearch'


def get_location(topic_id):
    province_dict = {}

    topic_dir = os.path.join(base_dir, 'topic' + str(topic_id))
    entity_dir = os.path.join(topic_dir, 'entity')
    event_base_dir = os.path.join(topic_dir, 'events')

    events_dir_list = os.listdir(event_base_dir)
    events_dir_list.sort(key=sort_key)

    for event_dir in events_dir_list:
        event_path = os.path.join(event_base_dir, event_dir)
        event_file = os.listdir(event_path)[0]

        # 获得‘topic0_doc10180.txt’里的文档id
        doc_id = int(re.findall('\\d+', event_file)[1])
        locations = get_loc_entity(topic_id, doc_id, entity_dir)
        if not locations:
            continue
        provinces = find_province(locations)
        for province in provinces:
            if province == '':
                continue
            province = get_short_name(province)
            count = province_dict.get(province, 0)
            province_dict[province] = count + 1

    return province_dict


def find_province(locations):
    df = cpca.transform(locations)
    provinces = df['省'].tolist()
    return provinces


def get_short_name(province):
    if '省' in province:
        return province[:-1]
    if '市' in province:
        return province[:-1]
    if '特别行政区' in province:
        return province[:-5]
    if '自治区' in province:
        if '壮族' in province:
            return province[:-5]
        if '维吾尔' in province:
            return province[:-6]
        if '回族' in province:
            return province[:-5]
        return province[:-3]


def get_loc_entity(topic_id, doc_id, entity_dir):
    entity_filename = 'topic' + str(topic_id) + '_entity' + str(doc_id) + '.txt'
    entity_path = os.path.join(entity_dir, entity_filename)
    with open(entity_path, 'r', encoding='utf-8') as f:
        words = f.readline().split()
        tags = f.readline().split()
    locations = []
    for i in range(len(tags)):
        if tags[i] == 'LOC':
            locations.append(words[i])
    return locations


def sort_key(s):
    """ 获得‘event1’里的数字"""
    if s:
        try:
            c = re.findall('\\d+', s)[0]
        except:
            c = -1
        return int(c)


if __name__ == '__main__':
    get_location(0)
