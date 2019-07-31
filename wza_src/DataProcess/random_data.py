import os
import random
import shutil

src_dir = 'data'
des_dir = 'data_random'


def get_data():
    is_exists = os.path.exists(des_dir)
    if not is_exists:
        os.makedirs(des_dir)
    file_list = [f for f in os.listdir(src_dir) if f.endswith('.txt')]
    file_list = file_list[200:]
    random.shuffle(file_list)
    file_list = file_list[:2000]
    for i, f in enumerate(file_list):
        src_path = os.path.join(src_dir, f)
        des_path = os.path.join(des_dir, 'news_content' + str(i+201) + '.txt')
        shutil.copy(src_path, des_path)


if __name__ == '__main__':
    get_data()
