from aip import AipImageClassify
import os
import wave
import numpy as np
import shutil
import os.path

def init_client():
    """
    初始设置
    :return:
    """
    APP_ID = ''
    API_KEY = ''
    SECRET_KEY = ''

    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
    return client


def del_file(path):
    """
    删除指定目录和目录下的所有文件
    :param path:
    :return:
    """
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
    shutil.rmtree(path)

def get_file(filename):
    """
    读取图片
    :param filename:
    :return:
    """
    with open(filename,'rb') as f:
        return f.read()

def is_animal(filename):
    """
    识别动物
    :param filename:
    :return:
    """
    image = get_file(filename)
    client = init_client()

    """ 如果有可选参数 """
    options = {}
    options["top_num"] = 3
    options["baike_num"] = 5

    """ 带参数调用动物识别 """
    result = (client.animalDetect(image, options))['result'][0]

    image_info = dict()
    image_info['name'] = result['name']
    if result['baike_info']: #若是动物
        #print('是动物')
        image_info['baike_url'] = result['baike_info']['baike_url']
        image_info['description'] = result['baike_info']['description']
        #print(image_info)
        return image_info
    else:
        #print('不是动物')
        return False

def is_dish(filename):
    """
    识别菜品
    :param filename:
    :return:
    """
    image = get_file(filename)
    client = init_client()

    """ 如果有可选参数 """
    options = {}
    options["top_num"] = 3
    options["filter_threshold"] = "0.7"
    options["baike_num"] = 5

    """ 带参数调用菜品识别 """
    result = (client.dishDetect(image, options))['result'][0]
    #print(result)


    dish_info = dict()
    dish_info['name'] = result['name']
    if result['baike_info']:
        #print('是菜品种类')
        dish_info['baike_url'] = result['baike_info']['baike_url']
        if 'description' in result['baike_info']:
            dish_info['description'] = result['baike_info']['description']
        #print(dish_info)
        return dish_info
    else:
        #print('不是菜品种类')
        return False

def if_other(filename):
    """
    通用识别
    :param filename:
    :return:
    """
    image = get_file(filename)
    client = init_client()

    """ 如果有可选参数 """
    options = {}
    options["baike_num"] = 5

    """ 带参数调用菜品识别 """
    result = (client.advancedGeneral(image, options))['result'][0]

    pic_info = dict()
    pic_info['name'] = result['keyword']
    pic_info['description'] = result['baike_info']['description']
    pic_info['baike_url'] = result['baike_info']['baike_url']

    #print(pic_info)
    return pic_info

def read_image(filename):
    print('--------------------')
    print(filename)
    info = dict()
    if is_animal(filename):
        print('属于动物')
        info = is_animal(filename)
    elif is_dish(filename):
        print('属于菜品种类')
        info = is_dish(filename)
    else:
        print('属于其他类别')
        info = if_other(filename)

    print('name:'+str(info['name']))
    print('baike_url:'+str(info['baike_url']))
    print('description:'+str(info['description']))
    print('--------------------')


if __name__=='__main__':
    read_image('文本数据提取/动物菜品识别/shu.jpg')
    # read_image('文本数据提取/动物菜品识别/dan.jpg')
    # read_image('文本数据提取/动物菜品识别/caomei.jpg')
    # read_image('文本数据提取/动物菜品识别/gou.jpg')






