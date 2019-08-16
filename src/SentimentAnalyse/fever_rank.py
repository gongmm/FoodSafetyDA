import os

from pyecharts.charts import Bar
from pyecharts import options as opts
import pyecharts.globals
from sklearn.externals import joblib

from sentiment_fever import calculate_fever_by_topic, calculate_three_part_by_month

chart_dir = 'chart'
model_dir = 'result'
if not os.path.exists(chart_dir):
    os.makedirs(chart_dir)
if not os.path.exists(model_dir):
    os.makedirs(model_dir)


def get_keyword_by_id(id):
    id_list = []
    word_list = []
    with open('keywords.txt', 'r') as f:
        for info in f.readlines():
            topic_id = info.split(',')[0]
            topic_word = info.split(',')[-1].strip()
            id_list.append(topic_id)
            word_list.append(topic_word)
    index = id_list.index(str(id))
    keyword = word_list[index]
    return keyword


def get_keywords():
    keywords = []
    with open('keywords.txt', 'r') as f:
        for info in f.readlines():
            keyword = info.split(',')[-1].strip()
            keywords.append(keyword)
    return keywords


def get_id_list():
    id_list = []
    with open('keywords.txt', 'r') as f:
        for info in f.readlines():
            topic_id = info.split(',')[0]
            id_list.append(topic_id)
    return id_list


def topic_fever_rank(month, topic_num=45):
    topic_fever_dict = {}
    id_list = get_id_list()
    for topic in range(topic_num):
        if str(topic) in id_list:
            fever_list = calculate_fever_by_topic(topic_id=topic, standardize=False)
            fever = fever_list[month - 1]
            keyword = get_keyword_by_id(topic)
            topic_fever_dict[keyword] = fever
    z = zip(topic_fever_dict.values(), topic_fever_dict.keys())
    result = sorted(z, reverse=True)
    # result = sorted(z)
    title = [t[-1] for t in result]
    value = [t[0] for t in result]
    joblib.dump(title, os.path.join(model_dir, 'title.list'))
    joblib.dump(value, os.path.join(model_dir, 'value.list'))
    return title, value


def topic_fever_rank_three_component(month, topic_num=45):
    result_fever, result_news, result_forum, result_weibo = calculate_three_part_by_month(month)
    keywords = get_keywords()
    z = zip(result_fever, result_news, result_forum, result_weibo, keywords)
    result = sorted(z, reverse=True)
    # result = sorted(z)
    title = [t[-1] for t in result]
    fever_value = [t[0] for t in result]
    news_value = [t[1] for t in result]
    forum_value = [t[2] for t in result]
    weibo_value = [t[3] for t in result]
    joblib.dump(title, os.path.join(model_dir, 'component_keyword.list'))
    joblib.dump(fever_value, os.path.join(model_dir, 'component_fever_value.list'))
    joblib.dump(news_value, os.path.join(model_dir, 'component_news_value.list'))
    joblib.dump(forum_value, os.path.join(model_dir, 'component_forum_value.list'))
    joblib.dump(weibo_value, os.path.join(model_dir, 'component_weibo_value.list'))
    return title, fever_value, news_value, forum_value, weibo_value


def draw_rank(month=8):
    if os.path.exists(os.path.join(model_dir, 'title.list')) and os.path.join(model_dir, 'value.list'):
        title = joblib.load(os.path.join(model_dir, 'title.list'))
        value = joblib.load(os.path.join(model_dir, 'value.list'))
    else:
        title, value = topic_fever_rank(month=month)
    fever_chart = chart_config(canvas_width='1500px',
                               canvas_height='700px',
                               tip_formats='{b}:{c}\n',
                               )
    fever_chart.add_xaxis(title)
    fever_chart.add_yaxis("8月份", value)
    # fever_chart.reversal_axis()
    fever_chart.set_series_opts(label_opts=opts.LabelOpts(position="top"))
    chart_path = os.path.join(chart_dir, 'fever_rank_chart.html')
    fever_chart.render(path=chart_path)


def draw_rank_with_three_component(month=8):
    if os.path.exists(os.path.join(model_dir, 'component_keyword.list')) \
            and os.path.join(model_dir, 'component_fever_value.list') \
            and os.path.join(model_dir, 'component_news_value.list')\
            and os.path.join(model_dir, 'component_forum_value.list')\
            and os.path.join(model_dir, 'component_weibo_value.list'):
        keywords = joblib.load(os.path.join(model_dir, 'component_keyword.list'))
        fever_values = joblib.load(os.path.join(model_dir, 'component_fever_value.list'))
        news_values = joblib.load(os.path.join(model_dir, 'component_news_value.list'))
        forum_values = joblib.load(os.path.join(model_dir, 'component_forum_value.list'))
        weibo_values = joblib.load(os.path.join(model_dir, 'component_weibo_value.list'))
    else:
        keywords, fever_values, news_values, forum_values, weibo_values = topic_fever_rank_three_component(month=month)
    fever_chart = chart_config(canvas_width='1500px',
                               canvas_height='700px',
                               tip_formats='{b}:{c}\n',
                               )
    fever_chart.add_xaxis(keywords)
    fever_chart.add_yaxis("新闻", news_values, stack="stack1")
    fever_chart.add_yaxis("食品论坛", forum_values, stack="stack1")
    fever_chart.add_yaxis("微博", weibo_values, stack="stack1")
    # fever_chart.reversal_axis()
    fever_chart.set_series_opts(label_opts=opts.LabelOpts(position="top", is_show=False))
    chart_path = os.path.join(chart_dir, 'fever_rank_chart_three_component.html')
    fever_chart.render(path=chart_path)


def chart_config(canvas_width='800px', canvas_height='500px',
                 legend_type='plain', legend_pos_top=None, tip_formats=None):
    """图表设置

        第一个参数是画单个主题和所有主题地图都需要传递的参数，
        后面的参数供画所有主题地图使用，使得地图更好看。

        Args:
            canvas_width: 画布的宽度
            canvas_height: 画布的高度
            legend_type: 图例的类型，普通为'plain'，多图例时用'scroll'
            legend_pos_top: 图例距容器上方的距离
            tip_formats: 提示框的格式

        Returns:
            chart: 地图

        """
    chart = (
        Bar(init_opts=opts.InitOpts(width=canvas_width, height=canvas_height,
                                    page_title='8月话题热度排行榜'
                                    ))

            .set_global_opts(title_opts=opts.TitleOpts(title="8月话题热度排行榜"),
                             legend_opts=
                             opts.LegendOpts(type_=legend_type, pos_top=legend_pos_top),
                             tooltip_opts=opts.TooltipOpts(formatter=tip_formats),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0, interval=0)),
                             datazoom_opts=opts.DataZoomOpts(),
                             )
    )
    return chart


if __name__ == '__main__':
    cur_month = 8
    # rank_list = topic_fever_rank(cur_month)
    # print(rank_list)
    draw_rank()
    draw_rank_with_three_component()
