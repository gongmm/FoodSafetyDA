from aip import AipSpeech
import os
import wave
import numpy as np
from pydub import AudioSegment
import shutil
import os.path
import time

result_dir = 'words_result'

def init_client():
    """
    初始设置
    :return:
    """
    APP_ID = '16564133'
    API_KEY = 'jOXlr6E5BNc71h7uotcVmCjZ'
    SECRET_KEY = 'sDXVWij9qd3X4NBjroC49LjBO2h0t08I'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    return client

def wav2pcm(wav_path):
    """批量转换文件夹中的wav文件为pcm文件"""
    wav_file = os.listdir(wav_path)
    if '.DS_Store' in wav_file:
        index = wav_file.index('.DS_Store')
        wav_file.pop(index)

    # 保证文件顺序是正确的
    wav_file.sort()
    #print(wav_file)

    for i, wav in enumerate(wav_file):
        wav_name = os.path.join(wav_path, wav)
        os.system('ffmpeg -y  -i '+ wav_name +'  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 ' + wav_path + '/' + str(i) + '.pcm')
        os.remove(wav_name) # 删除文件夹中的wav文件

def pcm2word(filepath,client):
    """
    音频识别
    原始 PCM 的录音参数必须符合 8k/16k 采样率、16bit 位深、单声道，
    支持的格式有：pcm（不压缩）、wav（不压缩，pcm编码）、amr（压缩格式）。
    :param filepath: 单个pcm文件路径
    :param client:  初始化client
    :return: 识别的文字
    """
    #client = init_client()
    with open(filepath,'rb') as f:
        file = f.read()
    result = client.asr(file, 'pcm', 16000, {
        'dev_pid': 1537,   # 1536无标点
    })
    #print(result)

    if result['err_no']==0: #若无错误
        text = result['result'][0]  #读取识别结果
        #print(text)
        return text
    else:
        #print('错误编号%d'%result['err_no'])
        return ''

def getText(filename, wav):
    """
    识别音频中的文字
    :param filename: pcm文件夹路径
    :return:识别的文字
    """
    client = init_client()
    pcm_file = os.listdir(filename)

    # 保证文件顺序是正确的
    pcm_file.sort()
    #print(pcm_file)

    content = ''
    for i, pcm in enumerate(pcm_file):
        text = pcm2word(os.path.join(filename, pcm), client)
        content = content + text
 
    # 获得文件名
    result_file = os.path.splitext(wav)[0] + '.txt'
    with open(os.path.join(result_dir, result_file),'w') as f:
        f.write(content)
    return content

def cut_wav(wav_name, cutdir_name):
    """
    分割wav音频文件
    :param filename:wav音频文件路径
    :param cutdir_name:分割后文件夹路径
    :return:
    """
    # 设置分割时长间隔
    cuttime = 60
    print(wav_name)
    f = wave.open(wav_name, 'rb')

    #读取格式信息，返回tuple(声道数，采样宽度，采样频率，采样点数，压缩类型，压缩类型描述)
    params = f.getparams()

    #只取前四个信息
    nchannels, sampwidth, framerate, nframes = params[:4]

    #分割采样数=采样率*分割时间
    cutframenum = framerate*cuttime

    #将波形数据转化为数组
    str_data = f.readframes(nframes)
    f.close()
    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    temp_data = wave_data.T

    StepNum = cutframenum   #步长
    StepTotalNum = 0   #采样帧数计数
    count = 0   #计数器

    # 对音频文件进行分割
    while StepTotalNum < nframes:
        # 设置分割后的文件路径
        FileName = os.path.join(cutdir_name, str(count) + '.wav')

        temp_dataTemp = temp_data[StepNum * (count):StepNum * (count + 1)]
        count = count + 1;
        StepTotalNum = count * StepNum;
        temp_dataTemp.shape = 1, -1
        temp_dataTemp = temp_dataTemp.astype(np.short)  # 打开WAV文档
        f = wave.open(FileName, "wb")
        # 配置声道数、量化位数和取样频率
        f.setnchannels(nchannels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        # 将wav_data转换为二进制数据写入文件
        f.writeframes(temp_dataTemp.tostring())
        f.close()

def del_file(path):
    """删除指定目录和目录下的所有文件"""
    shutil.rmtree(path)

def audio2text(wav_path):
    """
    遍历wav文件夹，识别每个wav的文字内容
    :param wav_path: wav文件夹路径
    """
    wav_file = os.listdir(wav_path)
    # 排除.DS_Store文件
    if '.DS_Store' in wav_file:
        index = wav_file.index('.DS_Store')
        wav_file.pop(index)
    for i,wav in enumerate(wav_file): 
        print(wav)
        # 生成的分割文件夹路径
        newdirname = os.path.join(wav_path, str(i+1))

        try:
            # 为每个音频创造一个文件夹存储分割后的音频
            os.mkdir(newdirname)

            # 原wav文件路径
            wav_name = os.path.join(wav_path, wav)

            # 切割wav文件
            print('______分割wav文件______')
            cut_wav(wav_name, newdirname)

            # 将wav文件全部转换为pcm文件
            print('______wav转化为pcm______')
            wav2pcm(newdirname)

            # 提取pcm文件夹中所有pcm文件的文字
            print('______音频提取文字______')
            text = getText(newdirname, wav)
            print(text)

        except Exception as err:
            print(err)
        finally:
            #删除生成的文件夹
            del_file(newdirname)

def audio_process(wav_path):
    """处理音频"""
    print('提取文字开始')
     #创建一个文件夹存放识别结果
    if result_dir not in os.listdir():
        os.mkdir(result_dir)
    audio2text(wav_path)


if __name__=='__main__':
    print('________________________________')
    print('音频识别开始')
    t_begin = time.time()
    audio_process('wav_audios')
    t_end = time.time()
    print('音频识别结束')
    t = t_end-t_begin
    print('程序消耗时间：'+str(t))
    print('________________________________')
