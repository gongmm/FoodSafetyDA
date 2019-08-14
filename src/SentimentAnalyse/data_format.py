import os
import pandas as pd

import chardet

origin_path = 'origin_data'
format_path = 'format_data'


def get_encoding(file):
    """ 获取文件编码类型 """
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        data = f.read()
        return chardet.detect(data)['encoding']


def gbk_2_utf(readfile, tmp_file='tmp'):
    """ 读取gbk格式的文件转码为utf-8格式 """
    tmp_file = os.path.join(origin_path, tmp_file)
    try:
        with open(readfile, 'r', encoding="GB18030") as f:
            with open(tmp_file, 'w', encoding='utf-8') as f_w:
                for row in f:
                    row = row.encode("utf-8").decode("utf-8")
                    f_w.write(row)
    except Exception as e:
        print(e)
        os.remove(tmp_file)
    else:
        os.remove(readfile)
        os.rename(tmp_file, readfile)


def reformat_date(readfile, writefile):
    """ 格式化文件中的日期格式 """
    # 读csv文件
    df = pd.read_csv(readfile)
    for i in range(df['pub_date'].shape[0]):
        # for row in df['pub_date']:
        try:
            df.loc[i, 'pub_date'] = df.loc[i, 'pub_date'].replace('年', '/')
            df.loc[i, 'pub_date'] = df.loc[i, 'pub_date'].replace('月', '/')
            df.loc[i, 'pub_date'] = df.loc[i, 'pub_date'].replace('日', '')
        except:
            print(i)
    df['pub_date'] = pd.to_datetime(df['pub_date'])  # 将数据类型转换为日期类型
    df.to_csv(writefile)


def format_data():
    """ 文件格式化：转码、格式化日期 """
    files = os.listdir(origin_path)
    # 进行转码
    for file in files:
        file_path = os.path.join(origin_path, file)
        result_path = os.path.join(format_path, file)
        gbk_2_utf(file_path)
        reformat_date(file_path, result_path)


if __name__ == '__main__':
    format_data()
