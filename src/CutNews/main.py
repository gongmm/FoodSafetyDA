import os
import re

file_path = "anns_data/"
origin_train_path = "data/food.train"
origin_test_path = "data/food.test"
origin_dev_path = "data/food.dev"


def split_train_test_dev():
    """
    数据集切分：将数据集按照7：2：1的比例划分为训练集、测试集、开发集
    :return:
    """
    path_dir = os.listdir(file_path)
    sum_num = len(path_dir)
    for index, filename in enumerate(path_dir):
        child = os.path.join('%s%s' % (file_path, filename))
        if index < sum_num * 0.7:
            with open(origin_train_path, 'a+', encoding='utf-8') as fw:
                with open(child, 'r', encoding='utf-8') as fr:
                    anns = fr.read()
                    # 去掉错误标记的行
                    anns = re.sub('\n\s*O\n+', '\n', anns)
                fw.write(anns)
        elif sum_num * 0.7 <= index < sum_num * 0.9:
            with open(origin_test_path, 'a+', encoding='utf-8') as fw:
                with open(child, 'r', encoding='utf-8') as fr:
                    anns = fr.read()
                    anns = re.sub('\n\s*O\n+', '\n', anns)
                fw.write(anns)
        elif index > sum_num * 0.9:
            with open(origin_dev_path, 'a+', encoding='utf-8') as fw:
                with open(child, 'r', encoding='utf-8') as fr:
                    anns = fr.read()
                    anns = re.sub('\n\s*O\n+', '\n', anns)
                fw.write(anns)


def cut_file(readfile, writefile):
    """
    切分长新闻
    :param readfile:
    :param writefile:
    :return:
    """
    with open(readfile, "r", encoding="utf-8") as food_dev_file:
        with open(writefile, "a+", encoding="utf-8") as write_file:
            write_file.truncate()
            begin_line = 0
            end_line = 0
            for line in food_dev_file:
                end_line += 1
                first_char = line[0]
                write_file.writelines(line)
                if (first_char == "。" or first_char == "，" or first_char == "？") and end_line - begin_line > 20:
                    begin_line = 0
                    end_line = 0
                    write_file.writelines("\n")

                print(first_char)


if __name__ == "__main__":
    split_train_test_dev()
    cut_file(origin_train_path, "data/new_food.train")
    cut_file(origin_test_path, "data/new_food.test")
    cut_file(origin_dev_path, "data/new_food.dev")
