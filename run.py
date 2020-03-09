#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/9/3 23:14
@Desc   ：
=================================================='''
from flask import Flask, render_template, request
from similar_said.speechExtract import del_sentences
from config.log_config import logger
import jieba
import base64
import re

app = Flask(__name__, template_folder='templates', static_folder='static')


def base64_encode(s):
    return base64.encodebytes(s.encode()).decode().replace('\n', '').replace('/', '_').replace("+", '-')


def base64_decode(base64_str):
    base64_str = base64_str.replace('_', '/').replace("-", '+')
    return base64.decodebytes(base64_str.encode()).decode()


def get_fly_words(fly_str):
    fly_words = []
    for x in re.findall(r'\w+', fly_str):
        fly_words += jieba.lcut(x)
    return {
        'wordList': fly_words,
    }


@app.route('/fly-words')
def fly_words():
    fly_str_base64 = request.args.get('s')
    fly_str = ''
    try:
        fly_str = base64_decode(fly_str_base64)
    except:
        pass
    if not fly_str:
        fly_str = fly_str_base64
    if not fly_str:
        fly_str = "没有内容"
    return render_template('fly_words.html', **get_fly_words(fly_str))


# 展示网站主页
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/SpeechExtraction')
def index():
    fly_str = """
        新闻人物言论自动提取。 
        新闻人物言论即是在报道的新闻中，某个人物、团体或机构在某个时间、某个地点表达某种观点、意见或态度。
        面对互联网信息量的不断扩张，用户迫切地需要自动化的信息获取工具来帮助在海量的信息源中迅速找到和获得真正所需的信息。主要相关方面的研究有自动摘要、关键词提取以及人物言论的自动提取，这些都可以帮助用户快速准确的获取其所需的真正信息，节省用户时间，提高用户体验。其中新闻人物言论自动提取就可以帮助用户在新闻阅读、观点总结中能够发挥较大的辅助作用。
    """
    return render_template('index.html', fly_str=base64_encode(fly_str))


@app.route('/extra', methods=['GET', 'POST'])
def extra():
    if request.method == 'GET':
        news = request.args.get('s')
    elif request.method == 'POST':
        news = request.form['news']
    else:
        news = ''
    logger.info(news)
    if not news:
        # return '<script>alert("没有输入内容！")</script>'
        news = "国台办表示中国必然统一。会尽最大努力争取和平统一，但绝不承诺放弃使用武力。台湾人民说回归中国好啊"
    news_parse = del_sentences(news)
    logger.info(news_parse)
    if isinstance(news_parse, list):
        infos_type = "list"
        logger.info('parse is list')
    else:
        infos_type = 'str'
        logger.info('parse is str')
    return render_template('extra.html', infos=news_parse, infos_type=infos_type, fly_str=base64_encode(news[:500]))


if __name__ == "__main__":
    app.debug = True
    jieba.initialize()
    app.run(host='0.0.0.0', debug=True, port=8088)
