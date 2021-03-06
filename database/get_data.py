#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/8/20 20:03
@Desc   ：连接数据库，读取数据
=================================================='''
import pymysql
import re
import pysnooper
# 从config配置中读取数据库配置
from config.get_db_info import GetConfParams
# 从config配置中读取news_sentences_xut文件路径
from config.file_path import path_news_sentences_xut_txt

# 实例化读取配置对象，日志对象
ConfParams = GetConfParams()
logger = ConfParams.logger


def clean(s):
    """
    清洗数据
    :param s: 文本
    :return:
    """
    re_compile = re.compile(r'�|《|》|\/|）|（|【|】|\\n|\\r|\\t|\\u3000|;|\*')
    string = re_compile.sub('', str(s))
    return string


# 从数据库中得到新闻语料库
@pysnooper.snoop()
def get_news_from_sql(host, user, password, database, port):
    logger.info('开始连接数据库...')
    db = pymysql.connect(host, user, password, database, port, charset='utf8')  # 不添加charset，读取到的数据是乱码
    logger.info('连接成功...')

    cursor = db.cursor()
    sql = """SELECT content from news_chinese"""
    try:
        cursor.execute(sql)
    except Exception as e:
        # 如果发生异常，则回滚
        logger.error("发生异常", e)
        db.rollback()
        return

    news = cursor.fetchall()
    print(len(news))
    cursor.close()
    db.close()

    return news

    # 同样的代码，save_txt的代码写到get_news_from_sql的最后面，保存文本慢得要死，一行一行地读取数据
    # 将代码分开写成函数，速度一下子提升上万倍，一下子就保存好了


def save_txt(news, file_name=None):
    if file_name is None:
        file_name = path_news_sentences_xut_txt
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            for content in news:
                data = content[0]
                text = clean(data)
                f.write(text + '\n')
    except Exception as w:
        logger.error('保存数据到文本出现问题', w)


if __name__ == "__main__":
    # 从config配置文件中读取数据库信息
    host = ConfParams.host
    user = ConfParams.user
    password = ConfParams.password
    database = ConfParams.db_name
    port = ConfParams.port

    try:
        contents = get_news_from_sql(host, user, password, database, port)
        save_txt(contents)
    except Exception:
        # 如果发生异常，则回滚
        logger.error("ERROR", Exception)
        # db.rollback()
        pass
