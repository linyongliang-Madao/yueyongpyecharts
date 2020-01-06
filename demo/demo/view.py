from django.http import HttpResponse
import csv
import pandas as pd
from django.shortcuts import render
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Pie, Timeline,Map
from django.template import loader
from pyecharts import options as opts
from pyecharts.charts import Line
import plotly as py
import plotly.graph_objs as go
import pandas as pd
import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout, Data

def hello(request):
    return HttpResponse("Welcome to my paradise ! ")


def dfdemo():
    # 读取国际旅游收入的csv文档数据
    df = pd.read_csv("templates\csvfile\API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_612605.csv")
    # 只读取数据中‘world’（257）行的数据
    data = df[-7:-6]
    # print(data)
    # 缺失值用0代替但下面无缺失值
    # data1=data.fillna(0)
    # data1
    data2 = data[['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']]
    # print(data2)
    # 整理每年的世界平均值
    data3 = data2.iloc[-1]
    # print(data3)
    return df


def timeline_map() -> Timeline:
    tl = Timeline()
    df = dfdemo()
    for i in range(2009, 2018):
        map0 = (
            Map()
                .add(
                "国际旅游收入", list(zip(list(df.CountryName), list(df["{}".format(i)]))), "world", is_map_symbol_show=False
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="2009-2017年世界各国国际旅游收入（占总出口的百分比）".format(i),
                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="red", font_size=10,
                                                                                     font_style="italic")),

                visualmap_opts=opts.VisualMapOpts(series_index=0, max_=20),

            )
        )
        tl.add(map0, "{}".format(i))
    return tl

def pdmapdemo(request):
    tl = timeline_map()
    tl.render(r"templates\templates\pdmap.html")
    static_html = r"templates\pdmap.html"
    print(static_html)
    # template = loader.get_template('templates/pdmap.html')
    return render(request,static_html)


def Line_base() -> Line:
    df = dfdemo()
    data = df[-7:-6]
    data2 = data[['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']]
    data3 = data2.iloc[-1]
    x = ["{}".format(i) for i in range(2009, 2018)]
    c = (
        Line()
            .add_xaxis(x)
            .add_yaxis("国家旅游收入（占总出口的百分比）", data3,
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),

                       )
            .set_global_opts(title_opts=opts.TitleOpts(title="国家旅游收入（占总出口的百分比）", subtitle="2009年～2018年"))
    )
    return c

def avgpdmapdemo(request):
    tl = Line_base()
    tl.render(r"templates\templates\avgpdmap.html")
    static_html = r"templates\avgpdmap.html"
    print(static_html)
    # template = loader.get_template('templates/pdmap.html')
    return render(request,static_html)

#读取中国旅游业发展数据
def travel():
    py.offline.init_notebook_mode()
    df = pd.read_csv("templates\csvfile\\tourism develop.csv")
    return df

def retravel(request):
    df = travel()
    df = df[-2:]
    dfc = df.set_index('指标')
    internationalTourism = go.Scatter(
    x=[pd.to_datetime('01/01/{y}'.format(y=x), format="%m/%d/%Y") for x in dfc.columns.values],
    y=dfc.loc["国际旅游外汇收入",:].values,
    name = "国际旅游外汇收入"
)
    domesticConsumption = go.Scatter(
    x=[pd.to_datetime('01/01/{y}'.format(y=x), format="%m/%d/%Y") for x in dfc.columns.values],
    y=dfc.loc["国内旅游总花费",:].values,
    name = "国内旅游总花费"
)
    layout = dict(xaxis=dict(rangeselector=dict(buttons=list([
        dict(count=3,
             label="3年",
             step="year",
             stepmode="backward"),
        dict(count=5,
             label="5年",
             step="year",
             stepmode="backward"),
        dict(count=10,
             label="10年",
             step="year",
             stepmode="backward"),
    ])),
        rangeslider=dict(bgcolor="#70EC57"),
        title='年份'
    ),
        yaxis=dict(title='金额'),
        title="中国旅游业发展"
    )

    fig = dict(data=[internationalTourism, domesticConsumption], layout=layout)
    py.offline.plot(fig, filename="templates\\templates\中国旅游业.html")
    static_html = r"templates\中国旅游业.html"
    return render(request, static_html)

def GNIdemo(request):
    py.offline.init_notebook_mode()
    df = pd.read_csv("templates\csvfile\Household consumption level.csv")
    df = df[0:1]
    dfa = df.set_index('指标')
    dfa_nowdate = dfa.columns
    dfa_consumptionLevel = dfa.loc['居民消费水平', :].values
    dfa_name = dfa.loc['居民消费水平', :].name
    df1 = pd.read_csv("templates\csvfile\GNI.csv")
    df1 = df1[0:1]
    df1 = df1.set_index('指标')
    df1_consumptionLevel = df1.loc['国民总收入', :].values
    df1_name = df1.index
    print(dfa_name,df1_name)
    中国居民消费水平 = go.Bar(
        x=dfa_nowdate,
        y=dfa_consumptionLevel,
        name= '中国居民消费水平',
    )
    中国国民总收入 = go.Scatter(
        x=dfa_nowdate,
        y=df1_consumptionLevel,
        name='中国国民总收入',
        xaxis='x',
        yaxis='y2'  # 标明设置一个不同于trace1的一个坐标轴
    )

    data = [中国居民消费水平, 中国国民总收入]
    layout = go.Layout(
        yaxis2=dict(anchor='x', overlaying='y', side='right')  # 设置坐标轴的格式，一般次坐标轴在右侧
    )

    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig,filename="templates\\templates\中国国民总收入、消费.html")
    static_html = r"templates\中国国民总收入、消费.html"
    return render(request, static_html)

def railway(request):
    py.offline.init_notebook_mode()
    df1 = pd.read_csv("templates\csvfile\passenger capacity.csv")
    df1 = df1.fillna(0)
    df2 = df1.set_index('指标')
    df2.T.plot(kind="bar", xTitle="年份", yTitle="运输量",filename="templates\\templates\中国运输客运量.html")
    static_html = r"templates\中国运输客运量.html"
    return render(request, static_html)
