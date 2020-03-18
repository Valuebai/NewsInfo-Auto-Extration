#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2020/3/17 17:32
# @Software: PyCharm
# @Author  : https://github.com/Valuebai/
"""
    悬赏球体用到的工具函数
    ~~~~~~~~~~~~~~~

"""
import base64
import jieba
import re


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
