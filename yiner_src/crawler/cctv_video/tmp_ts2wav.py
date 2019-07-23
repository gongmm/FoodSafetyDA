import os

base_dir = 'ts_videos'
dir_name = 'wav_audios'


def sort_key(s):
    if s:
        try:
            c = re.findall('\d+', s)[0]
        except:
            c = -1
        return int(c)

def ts_to_wav(title):
        # 检测是否已存在wav文件
        video_dir = os.path.split(title)[-1]
        filename = os.path.join(dir_name, video_dir + '.wav')
        if dir_name not in os.listdir():
            os.makedirs(dir_name)
        elif os.path.isfile(filename):
            print('wav文件已存在')
            return

        # 开始格式转换
        print('ts文件正在进行转录wav......')
        dir_list = os.listdir(title)
        if '.DS_Store' in dir_list:
            index = dir_list.index('.DS_Store')
            dir_list.pop(index)
        dir_list.sort(key=sort_key)
        for index, file in enumerate(dir_list):
            file = os.path.join(title, file)
            dir_list[index] = file
        dirs = '|'.join(dir_list) 
        dirs = 'concat:' + dirs
        # wav的格式必须是pcm_s16le
        str = 'ffmpeg -y -i "' + dirs + '" -vn -acodec pcm_s16le -f wav -ar 16000 ' + filename
        os.system(str)

        print(filename)
        if os.path.isfile(filename):
            print('转换完成')

if __name__ == '__main__':
    dir_list = os.listdir(base_dir)
    for d in dir_list:
        title = os.path.join(base_dir, d)
        ts_to_wav(title)