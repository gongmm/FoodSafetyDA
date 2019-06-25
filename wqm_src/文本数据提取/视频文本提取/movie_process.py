from aip import AipOcr
import os
import wave
import numpy as np
from pydub import AudioSegment
import shutil
import os.path
import pylab
import imageio
import base64
import time
import random
import re
import matplotlib as plt
from PIL import Image
from urllib.request import urlopen
import ssl

def init_client():
    """
    初始设置
    :return:
    """
    APP_ID = '16564133'
    API_KEY = 'jOXlr6E5BNc71h7uotcVmCjZ'
    SECRET_KEY = 'sDXVWij9qd3X4NBjroC49LjBO2h0t08I'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    return client

def get_file(filename):
    """
    读取图片
    :param filename:
    :return:
    """
    with open(filename,'rb') as f:
        return f.read()

def get_words(client,options,imagepath,resultpath):
    """
    读取图片中的文字
    :param client:
    :param options:可选参数
    :param imagepath:图片路径
    :param resultpath:保存的结果路径
    :return:
    """
    image = get_file(imagepath)

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    #print(client.basicGeneral(image, options))
    result_list = (client.basicGeneral(image, options))['words_result']

    """将识别到的结果保存在txt文件中"""
    f = open(resultpath,'a') #a表示文本可以追加
    for result in result_list:
        #result = result.decode("utf-8")
        #print(result['words'])
        f.write(result['words'])
    f.close()



def cut_movie(mvurl,picpath):
    """
    截取视频帧并保存至文件夹内
    :param mvurl:视频url链接
    :param picpath: 图片文件夹路径
    :return:
    """
    interval = 50   #设置提取图片的帧数间隔
    #reader = imageio.get_reader(mvpath,  'ffmpeg')   #读取视频文件
    reader = imageio.get_reader(imageio.core.urlopen(mvurl).read(), 'ffmpeg')  # 直接根据mv的url读取视频文件
    size = len(reader)  #获取视频总帧数
    print('获取视频成功'+str(size))
    #每50帧提取一张图片
    for i in range(interval,size,interval):
        image = reader.get_data(i)

        height = image.shape[0]
        width = image.shape[1]

        roi = image[height-120:height,0:width,:]    #提取字幕区域（需要对字幕区域进行估计）
        pylab.imshow(roi)

        pylab.axis('off') #不显示坐标轴
        pylab.savefig(picpath + '/' + str(i) + '.jpg')  # 保存图片到指定目录

def read_movie(mvurl,resultname):
    picpath = resultname+'_pic'
    if not os.path.exists(picpath):
        os.mkdir(picpath)
        cut_movie(mvurl,picpath)

    client = init_client()  #初始化client
    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"


    """遍历存放分割好的图片文件夹，对每个图片进行识别"""
    for parent, dirnames, filenames in os.walk(picpath, followlinks=True):
        for filename in filenames[1:]:
            imagepath = os.path.join(parent, filename)
            #print(imagepath)
            get_words(client,options,imagepath,resultname)


if __name__=='__main__':

    movieurl = 'http://video.pearvideo.com/mp4/adshort/20180812/cont-1410146-12651268_adpkg-ad_hd.mp4'

    print('________________________________')
    print('视频文字提取开始')
    t_begin = time.time()
    read_movie(movieurl,'文本数据提取/视频文本提取/result.txt')
    t_end = time.time()
    print('视频文字提取结束')
    t = t_end-t_begin
    print('程序消耗时间：'+str(t))

    print('视频文字提取结果：')
    with open('文本数据提取/视频文本提取/result.txt','r') as f:
        print(f.read())
    print('________________________________')
    #get_words('1.jpg','1.txt')