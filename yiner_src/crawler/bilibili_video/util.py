import os
import pandas as pd
import numpy as np

wav_dir = 'wav_audios'

if __name__ == '__main__':
    result_dir = 'csv'
    result_file = 'bilibili_videos.csv'
    csv_path = os.path.join(result_dir, result_file)
    data = pd.read_csv(csv_path, encoding='gbk')
    aid_list = data['aid'].values
    file_list = os.listdir(wav_dir)

    for file in file_list:
        print(file)
        aid = int(os.path.splitext(file)[0])
        if not ((aid == aid_list).any()):
            path = os.path.join(wav_dir, file)
            os.remove(path)