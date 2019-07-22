import csv
import os

def txt2csv(src_dir, des_dir, csv_name):
    if src_dir not in os.listdir():
        print('文件夹%s不存在' %src_dir)
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
    headers = ['topic', 'content']



    if des_dir not in os.listdir():
        os.mkdir(des_dir)
    path = os.path.join(des_dir, csv_name)
    with open(path, 'w', encoding='utf-8') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
    print('转换成功！')

if __name__ == '__main__':
    src_dir = 'words_result'
    des_dir = 'csv'
    csv_name = 'cctv_news.csv'
    txt2csv(src_dir, des_dir, csv_name)
