#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/9/3 23:14
@Desc   ：
=================================================='''
import jieba
from flask import Flask, render_template, request
from config.log_config import logger
from common.ball_fly_words import base64_decode, base64_encode, get_fly_words
from common.pyltp_model import LtpModel
from config.file_path import LTP_DATA_DIR  # pyltp的存放路径

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/fly-words', methods=['GET', 'POST'])
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
@app.route('/home', methods=['GET', 'POST'])
def home():
    logger.info('访问/home 主页')
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
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
    news_parse = ltp_manager.get_sentences_json_result(news)
    logger.info(news_parse)
    if isinstance(news_parse, list):
        infos_type = "list"
        logger.info('parse is list')
    else:
        infos_type = 'str'
        logger.info('parse is str')
        logger.info(infos_type)
    return render_template('extra.html', infos=news_parse, infos_type=infos_type, fly_str=base64_encode(news[:500]))


if __name__ == "__main__":
    logger.info('初始化pyLtpModel')
    ltp_manager = LtpModel(LTP_DATA_DIR)
    logger.info('初始化jiebaModel')
    jieba.initialize()
    app.run(host='0.0.0.0', port=8088)
