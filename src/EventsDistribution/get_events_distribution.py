import os
import re
import cpca

base_dir = os.path.join('..', 'DataProcess', 'topic_doc')

# 搜索省份的网址
seach_url = 'http://xzqh.mca.gov.cn/fuzzySearch'


def get_location(topic_id):
    """根据主题id，获得对应主题下每个事件的发生省份。

    每个事件选取第一个文档作为代表，找到对应文档的实体文件，
    获取其中的地点实体，然后据此获取省份信息。
    注：没有地点实体或无法通过地点实体找到省份的直接跳过。

    Args:
        topic_id: 主题id

    Returns:
        province_dict: {省份:发送次数}字典
    """
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
    """调用库从地点实体获得省份信息

    Args:
        locations: 地点实体列表

    Returns:
        provinces: 省份全称列表
    """
    df = cpca.transform(locations)
    provinces = df['省'].tolist()
    return provinces


def get_short_name(province):
    """去掉省份中的后缀名，如“省”、“市”等，仅保留名称。

    Args:
        province: 省份全称列表

    Returns:
        province: 省份名称列表
    """
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
    """从实体文件中读入标签为LOC的名词作为地点实体。

    Args:
        topic_id: 主题id
        doc_id: 文档id
        entity_dir: 实体文件夹的路径

    Returns:
        locations: 地点实体列表
    """
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
    """获得‘event1’里的数字"""
    if s:
        try:
            c = re.findall('\\d+', s)[0]
        except:
            c = -1
        return int(c)


if __name__ == '__main__':
    get_location(0)
