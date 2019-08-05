import pandas as pd
import os


def txt2csv(src_dir, des_dir, csv_name):
    if src_dir not in os.listdir():
        print('文件夹%s不存在' % src_dir)
        return
    txt_list = os.listdir(src_dir)
    if '.DS_Store' in txt_list:
        index = txt_list.index('.DS_Store')
        txt_list.pop(index)
    if len(txt_list) == 0:
        print('没有txt文本')
        return

    rows = []

    for txt in txt_list:
        path = os.path.join(src_dir, txt)
        with open(path, 'r', encoding='gbk') as f:
            content = f.read()
        row = [txt[:-4], content]
        rows.append(row)

    if des_dir not in os.listdir():
        print('文件夹%s不存在' % des_dir)
        return

    csv_path = os.path.join(des_dir, csv_name)
    data = pd.read_csv(csv_path, encoding='gbk')

    # 除去空格
    for i in range(len(data)):
        raw_title = data.loc[i, 'title']
        raw_title = ''.join(raw_title.split())
        data.loc[i, 'title'] = raw_title

    # 插入内容
    for row in rows:
        title = row[0]
        content = row[1]
        data.loc[data['title'] == title, 'content'] = content
    data.to_csv(csv_path, encoding='gbk', index=False)
    print('成功保存内容至csv文件！')


if __name__ == '__main__':
    src_dir = 'words_result'
    des_dir = 'csv'
    csv_name = 'cctv_videos.csv'
    txt2csv(src_dir, des_dir, csv_name)
