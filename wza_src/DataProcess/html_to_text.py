import csv
import re


def html_to_text(readfile, writefile):
    with open(readfile, 'r', encoding='gbk') as f:
        with open(writefile, 'w', encoding='utf-8', newline='') as f1:
            rows = csv.reader(f)
            writer = csv.writer(f1)
            for row in rows:
                content_without_tag = re.sub(r'<.*?>', '', row[-1])
                row[-1] = content_without_tag.replace('\\n', '').strip()
                print(row)
                writer.writerow(row)


if __name__ == '__main__':
    html_to_text('wechat.csv', 'wechat_new.csv')
