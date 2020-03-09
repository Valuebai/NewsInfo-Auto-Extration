#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2020/3/9 16:05
# @Software: PyCharm
# @Author  : https://github.com/Valuebai/
"""
    <moudule>.name
    ~~~~~~~~~~~~~~~

    加载pyltp模型，提高性能
"""
import os
from config.file_path import LTP_DATA_DIR
from pyltp import Parser, NamedEntityRecognizer
from pyltp import Postagger

# 加载ltp模型目录的路径
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 依存句法分析模型路径，模型名称为`ner.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')

recognizer = NamedEntityRecognizer()  # 初始化实例
# recognizer.load(ner_model_path)  # 加载模型

parser = Parser()  # 初始化实例
# parser.load(par_model_path)  # 加载模型


postagger = Postagger()
# postagger.load(pos_model_path)
