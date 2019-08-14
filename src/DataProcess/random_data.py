import os
import random
import shutil

src_dir = 'data/regular'
des_dir = 'data_random'


def get_data(choose_num):
    """
    从所有的新闻文本中选取choose_num条新闻，用于标记
    Returns:

    """
    is_exists = os.path.exists(des_dir)
    if not is_exists:
        os.makedirs(des_dir)
    file_list = [f for f in os.listdir(src_dir) if f.endswith('.txt')]
    random.shuffle(file_list)
    file_list = file_list[:choose_num]
    for i, f in enumerate(file_list):
        src_path = os.path.join(src_dir, f)
        des_path = os.path.join(des_dir, 'news_content' + str(i) + '.txt')
        shutil.copy(src_path, des_path)


if __name__ == '__main__':
    get_data(choose_num=1000)
