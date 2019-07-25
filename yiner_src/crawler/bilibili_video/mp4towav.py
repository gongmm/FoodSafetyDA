import os

base_dir = 'mp4_videos'
dir_name = 'wav_audios'


def sort_key(s):
    if s:
        try:
            c = re.findall('\d+', s)[0]
        except:
            c = -1
        return int(c)

def mp4_to_wav(filename):
        # 检测是否已存在wav文件
        mp4_path = os.path.join(base_dir, filename)
        wav_path = os.path.join(dir_name, filename.split('.')[0] + '.wav')

        if dir_name not in os.listdir():
            os.makedirs(dir_name)
        elif os.path.isfile(wav_path):
            print('wav文件已存在')
            return

        # 开始格式转换
        print('mp4文件正在进行转录wav......')
        # dir_list = os.listdir(title)
        # if '.DS_Store' in dir_list:
        #     index = dir_list.index('.DS_Store')
        #     dir_list.pop(index)
        # dir_list.sort(key=sort_key)
        # for index, file in enumerate(dir_list):
        #     file = os.path.join(title, file)
        #     dir_list[index] = file
        # dirs = '|'.join(dir_list) 
        # dirs = 'concat:' + dirs

        # wav的格式必须是pcm_s16le
        str = 'ffmpeg -y -i "' + mp4_path + '" -vn -acodec pcm_s16le -f wav -ar 16000 ' + wav_path
        os.system(str)

        print(wav_path)
        if os.path.isfile(wav_path):
            print('转换完成')

if __name__ == '__main__':
    file_list = os.listdir(base_dir)
    for filename in file_list:
        mp4_to_wav(filename)