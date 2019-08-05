import os
import pandas as pd
import re
import pickle
import tensorflow as tf
from tqdm import tqdm

# call ChineseNER module
import sys
sys.path.append('..')  # 添加自己指定的搜索路径
sys.path.append('../ChineseNER')
from ChineseNER.model import Model
import ChineseNER.loader
import ChineseNER.utils
import ChineseNER.data_utils

# tensorflow config
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"       # 使用第二块GPU（从0开始）


# dic
result_dir = 'result'
model_dir = 'model'
vec_dir = 'vec_arr'
corpus_dir = 'corpus'
# 主题id-词文件，格式：[主题id, 词]
topic_word_csv = os.path.join(result_dir, 'food_topic_word.csv')
# 文档信息-主题id文件，格式：[文档信息, 主题id]
news_data_topic_csv = os.path.join(result_dir, 'all_news_data_utf_topic.csv')
# 文档id-主题id文件，格式：[文档id, 主题id]
doc_topic_csv = os.path.join(result_dir, 'doc_topic.csv')


def sort_key(s):
    if s:
        try:
            c = re.findall('\\d+', s)[1]
        except:
            c = -1
        return int(c)


def get_topic_doc():
    """将同一个主题的所有文档整理到相同文件夹中

    读取文档信息-主题id文件，对于每一个文档，将其内容写入对应的主题文件夹的txt文件中。
    """

    # 获得主题数
    topic_df = pd.read_csv(topic_word_csv)
    topic_num = topic_df.shape[0]

    # 将同一个主题的文档写入同一个文件夹的不同txt文件中
    # news_topic_df = pd.read_csv(news_data_topic_csv)
    doc_topic_df = pd.read_csv(doc_topic_csv)
    doc_num = doc_topic_df.shape[0]

    corpus_path = os.path.join(corpus_dir, 'news_content_corpus.txt')
    with open(corpus_path, 'r', encoding='utf-8') as f:
        doc_word_list = f.readlines()

    for i in range(doc_num):
        print('处理第%d个文档' % (i))
        # 判断文档对应的主题文件夹是否存在
        # content, title, topic_id = news_topic_df.loc[i, ['content', 'title', 'topic_id']]
        topic_id = doc_topic_df.loc[i, 'topic_id']

        line = doc_word_list[i]

        topic_dir = 'topic_doc/topic' + str(topic_id)
        is_exists = os.path.exists(topic_dir)
        # 如果不存在则创建目录
        if not is_exists:
            os.makedirs(topic_dir)

        file_path = 'topic_doc/topic' + str(topic_id) + \
                    '/topic' + str(topic_id) + '_doc' + str(i) + '.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            # 写入文件
            # print(line)
            f.write(line + '\n')  # 把这行写进文件

    return topic_num


def get_doc_entity(topic_num):
    """调用ChineseNER获得所有文档的命名实体

    获得所有文档的命名实体，将去重后的实体当成是分词，后续要送入doc2vec模型中训练。

    Args:
        topic_num: 主题的数量
    """

    with open('data/regular_total/news_content.txt', 'r', encoding='utf-8') as f:
        doc_contents = f.readlines()  # 一行文本
    for i in range(4, topic_num):
        print('————处理第%d个主题————' % i)
        # 读取一个主题中所有文档的文件名
        topic_dir = "topic_doc/topic" + str(i)
        doc_labels = [f for f in os.listdir(topic_dir) if f.endswith('.txt')]

        content_list = []
        file_path_list = []

        # 创建主题对应的entity文件夹
        entity_dir = os.path.join('topic_doc', 'topic' + str(i), 'entity')
        is_exists = os.path.exists(entity_dir)
        if not is_exists:
            os.makedirs(entity_dir)

        for doc_file in doc_labels:
            pattern = re.compile('doc\\d+')
            result = re.search(pattern, doc_file)
            if result:
                doc_id = result.group()[3:]  # 根据文件名获得文档id

                file_path = os.path.join(entity_dir, 'topic' + str(i) + '_entity' + str(doc_id) + '.txt')
                if os.path.exists(file_path):
                    print('%s文件已存在' % file_path)
                    continue

                # 获得预处理后的文本
                content = doc_contents[int(doc_id)]

                content_list.append(content)
                file_path_list.append(file_path)
            else:
                print('找不到文档文件！')

        # 批量送入ChineseNER模型中得到命名实体
        lines = evaluate_entities(content_list)

        # 批量写入文件
        for j in range(len(file_path_list)):
            with open(file_path_list[j], 'w', encoding='utf-8') as f:
                f.write(lines[j] + '\n')  # 把命名实体写进文件


def evaluate_entities(lines):
    """获得包含食品专有名词和其他命名实体的文本序列

    Args:
        lines: 预处理后的文档文本列表

    Returns:
        result: 带有命名实体的文本序列
    """
    # 重置默认图形，解决跑两次模型变量已经存在的问题
    tf.reset_default_graph()

    # food entities
    config_file = '../ChineseNER/food/config_file'
    log_file = '../ChineseNER/food/train.log'
    map_file = '../ChineseNER/food/maps.pkl'
    ckpt_path = '../ChineseNER/food/ckpt'
    food_result = evaluate_entities_core(lines, config_file, log_file, map_file, ckpt_path)

    # 重置默认图形，解决跑两次模型变量已经存在的问题
    tf.reset_default_graph()

    # other entities
    config_file = '../ChineseNER/other/config_file'
    log_file = '../ChineseNER/other/train.log'
    map_file = '../ChineseNER/other/maps.pkl'
    ckpt_path = '../ChineseNER/other/ckpt'
    other_result = evaluate_entities_core(lines, config_file, log_file, map_file, ckpt_path)

    # 将所有命名实体拼接起来
    result_list = []
    for i in range(len(food_result)):
        result = ' '.join(food_result[i] + other_result[i])
        result_list.append(result)

    return result_list


def evaluate_entities_core(lines, config_file='../ChineseNER/config_file', log_file='../ChineseNER/train.log',
                           map_file='../ChineseNER/maps.pkl', ckpt_path='../ChineseNER/ckpt'):
    """ 调用模型得到命名实体

        model.evaluate_line返回的result是一个字典，字典里的entities命名实体是list，list中每个元素是字典。字典格式为：
             result:
                     {
                     'string':'xxxxxxx',
                     'entities':[{x},{y}]
                     }
             其中，x:
                     {
                     'word':'三无产品',
                     'start':10,
                     'end':14,
                     'type':'Food'
                     }
        只取result['entities']加入列表result_list中。

    Args:
        lines: 预处理后的文档文本列表
        config_file: 配置文件路径
        log_file: 日志文件路径
        map_file: 映射文件路径
        ckpt_path: 模型文件路径

    Returns:
        result_list: 二维列表，其中result_list[i]是对应文档i的去重后的命名实体的列表。
    """
    config = ChineseNER.utils.load_config(config_file)
    logger = ChineseNER.utils.get_logger(log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(map_file, "rb") as f:
        char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        model = ChineseNER.utils.create_model(sess, Model, ckpt_path,
                                              ChineseNER.data_utils.load_word2vec, config, id_to_char, logger)
        result_list = []
        for line in tqdm(lines):
            result = model.evaluate_line(sess, ChineseNER.data_utils.input_from_line(line, char_to_id), id_to_tag)
            entities = list(set([f['word'] for f in result['entities']]))
            # print(entities)
            result_list.append(entities)

        return result_list

