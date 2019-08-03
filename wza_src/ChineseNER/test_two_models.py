# encoding=utf8
import os
import codecs
import pickle
import itertools
from collections import OrderedDict

import tensorflow as tf
import numpy as np
from model import Model
from loader import load_sentences, update_tag_scheme
from loader import char_mapping, tag_mapping
from loader import augment_with_pretrained, prepare_dataset
from utils import get_logger, make_path, clean, create_model, save_model
from utils import print_config, save_config, load_config, test_ner
from data_utils import load_word2vec, create_input, input_from_line, BatchManager


def evaluate_entities_core(line, config_file='../ChineseNER/config_file', log_file='../ChineseNER/train.log',
                           map_file='../ChineseNER/maps.pkl', ckpt_path='../ChineseNER/ckpt'):
    config = load_config(config_file)
    logger = get_logger(log_file)
    # limit GPU memory
    tf_config = tf.ConfigProto()
    tf_config.gpu_options.allow_growth = True
    with open(map_file, "rb") as f:
        char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)
    with tf.Session(config=tf_config) as sess:
        model = create_model(sess, Model, ckpt_path, load_word2vec, config, id_to_char, logger)
        result = model.evaluate_line(sess, input_from_line(line, char_to_id), id_to_tag)
        print(result)


if __name__ == "__main__":
    line = input("请输入测试句子:")
    evaluate_entities_core(line)
    # 清除默认图形堆栈并重置全局默认图形 解决同时跑两个模型存在的问题
    tf.reset_default_graph()
    evaluate_entities_core(line, config_file='../ChineseNER/backup/ckpt-others_0/config_file',
                           log_file='../ChineseNER/backup/ckpt-others_0/train.log',
                           map_file='../ChineseNER/backup/ckpt-others_0/maps.pkl',
                           ckpt_path='../ChineseNER/backup/ckpt-others_0/ckpt')
