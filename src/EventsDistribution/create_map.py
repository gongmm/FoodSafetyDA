import os
from functools import reduce
from sklearn.externals import joblib
from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from get_events_distribution import get_location

map_dir = 'map'
if not os.path.exists(map_dir):
    os.makedirs(map_dir)
dic_file = 'province_dic_list'


def create_map(topic_num):
    """为每个主题分别绘制热度图

    首先调用get_location函数获得每个话题的省份数据，
    再调用create_map_core函数添加数据到地图中，
    最后调用render函数渲染地图，真正绘制到html文件中。
    将所有主题的省份数据存储在文件中，供后续绘制包含所有主题数据的热度图使用。

    Args:
        topic_num: 主题的数量
    """
    province_dic_list = []
    for i in range(topic_num):
        province_distribution = get_location(i)
        province_dic_list.append(province_distribution)
        name = 'topic' + str(i)

        china_map = create_map_core(name, province_distribution)
        map_file = os.path.join(map_dir, 'topic' + str(i) + '_map.html')
        china_map.render(path=map_file)

    joblib.dump(province_dic_list, dic_file)


def create_total_map():
    """绘制包含所有主题数据的热度图

    从文件中读入所有主题的省份数据。
    """
    province_dic_list = joblib.load(dic_file)
    n = len(province_dic_list)
    name_list = ['topic'+str(i) for i in range(n)]
    china_map = create_map_list_core(name_list, province_dic_list)
    map_file = os.path.join(map_dir, 'total_map.html')
    china_map.render(path=map_file)


def create_map_core(name, dic):
    """为地图添加一种主题的数据

    Args:
        name: 数据系列的名称
        dic: 主题省份数据

    Returns:
        china_map: 地图
    """
    max_value = max(dic.values())
    china_map = map_config(max_value)
    china_map.add(name, [list(z) for z in zip(dic.keys(), dic.values())], 'china', is_roam=False, zoom=1.1)
    return china_map


def create_map_list_core(name_list, dic_list):
    """为地图添加所有主题的数据

    Args:
        name_list: 数据系列的名称列表
        dic_list: 主题省份数据列表

    Returns:
        china_map: 地图
    """
    # 字典合并过程会改变第一个字典，因此需要备份再替换
    first_dic = dic_list[0].copy()
    total_dic = merge_all_dict(dic_list)
    dic_list[0] = first_dic

    max_value = max(total_dic.values())
    china_map = map_config(max_value,
                           canvas_width='900px',
                           canvas_height='700px',
                           legend_type='scroll',
                           legend_pos_top='6%',
                           tip_formats='{b}:{c}\n',
                           )
    for i in range(len(dic_list)):
        name = name_list[i]
        dic = dic_list[i]
        china_map.add(name, [list(z) for z in zip(dic.keys(), dic.values())],
                      'china', is_map_symbol_show=False)
    return china_map


def map_config(max_value, canvas_width='800px', canvas_height='500px',
               legend_type='plain', legend_pos_top=None, tip_formats=None):
    """地图设置

    第一个参数是画单个主题和所有主题地图都需要传递的参数，
    后面的参数供画所有主题地图使用，使得地图更好看。

    Args:
        max_value: 热度最高值
        canvas_width: 画布的宽度
        canvas_height: 画布的高度
        legend_type: 图例的类型，普通为'plain'，多图例时用'scroll'
        legend_pos_top: 图例距容器上方的距离
        tip_formats: 提示框的格式

    Returns:
        china_map: 地图

    """
    china_map = (
        Map(init_opts=opts.InitOpts(width=canvas_width, height=canvas_height,
                                    page_title='事件地区分布热度图',
                                    theme=ThemeType.WESTEROS))
        .set_global_opts(title_opts=opts.TitleOpts(title="事件地区分布热度图"),
                         visualmap_opts=
                         opts.VisualMapOpts(
                                 max_=max_value,
                                 is_piecewise=True,
                                 pos_bottom='30%'),
                         legend_opts=
                         opts.LegendOpts(type_=legend_type, pos_top=legend_pos_top),
                         tooltip_opts=opts.TooltipOpts(formatter=tip_formats)
                         )
    )
    return china_map


def merge_all_dict(dict_list):
    """合并所有字典，相同键的值相加。

    reduce()函数会对参数序列中元素进行累积。
    用传给reduce中的函数function（有两个参数）先对集合中的第 1、2 个元素进行操作，
    得到的结果再与第三个数据用function函数运算，最后得到一个结果。
    注意：最后合并的字典是直接修改在列表中第一个字典，如果要保留原来的，需要提前深拷贝再替换掉。

    Args:
        dict_list: 字典列表

    Returns:
        dict: 合并后的字典
    """
    return reduce(merge, dict_list)


def merge(dict1, dict2):
    """合并两个字典，相同键的值相加。

    注意：这里合并后结果直接存在dict1中，因此dict1被修改，如果要保留原来的，需要提前深拷贝。

    Args:
        dict1: 字典1
        dict2: 字典2

    Returns:
        dict1: 合并后的字典
    """
    for i, j in dict2.items():
        if i in dict1.keys():
            dict1[i] += j
        else:
            dict1.update({f'{i}': dict2[i]})
    return dict1


if __name__ == '__main__':
    # create_map(45)
    create_total_map()
