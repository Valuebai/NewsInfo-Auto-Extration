#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time    : 2020/3/17 17:44
# @Software: PyCharm
# @Author  : https://github.com/Valuebai/
"""
    <封装pyltp model 类，方便使用>
    ~~~~~~~~~~~~~~~
"""
import os
import re
import jieba
import pysnooper

from similar_said.get_word_similar_said import txt_said  # 加载跟“说”有关的词
from config.file_path import LTP_DATA_DIR  # pyltp的存放路径

from pyltp import Segmentor  # pyltp 分词
from pyltp import SentenceSplitter  # pyltp 分句
from pyltp import Postagger  # pyltp 词性标注
from pyltp import NamedEntityRecognizer  # pyltp 命名实体识别
from pyltp import Parser  # 依存句法分析


class LtpModel(object):
    """
    封装pyltp model 类，方便使用
    """

    @pysnooper.snoop()
    def __init__(self, LTP_DATA_DIR):
        """加载pyltp模型"""
        self.LTP_DATA_DIR = LTP_DATA_DIR  # pyltp的存放路径

        # 分词模型路径，分词模型名称是 'cws.model'
        cws_model_path = os.path.join(self.LTP_DATA_DIR, 'cws.model')
        self.segmentor = Segmentor()
        self.segmentor.load(cws_model_path)

        # 词性标注模型路径，分词模型名称是 'pos.model'
        pos_model_path = os.path.join(self.LTP_DATA_DIR, 'pos.model')
        self.postager = Postagger()
        self.postager.load(pos_model_path)

        # 命名实体识别模型路径，模型名称为'ner.model'
        ner_model_path = os.path.join(self.LTP_DATA_DIR, 'ner.model')
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(ner_model_path)

        # 依存句法分析模型路径，模型名称为 'parser.model'
        par_model_path = os.path.join(self.LTP_DATA_DIR, 'parser.model')
        self.parser = Parser()
        self.parser.load(par_model_path)

        # # 语义角色标注模型目录路径，模型目录为'pisrl.model'
        # srl_model_path = os.path.join(self.LTP_DATA_DIR, 'pisrl.model')
        # self.labeller = SementicRoleLabeller()  # 初始化实例
        # self.labeller.load(srl_model_path)  # 加载模型

    def load_model(self):
        # """加载pyltp模型"""
        # # 分词模型路径，分词模型名称是‘cws.model’
        # self.segment = Segmentor()
        # print(cws_model_path)
        # self.segment.load(cws_model_path)

        # # 词性标注模型路径，分词模型名称是‘pos.model’
        # self.postager = Postagger()
        # self.postager.load(pos_model_path)
        #
        # # 命名实体识别模型路径，模型名称为`pos.model`
        # self.recognizer = NamedEntityRecognizer()
        # self.recognizer.load(ner_model_path)
        #
        # # 依存句法分析模型路径，模型名称为`parser.model`
        # self.parser = Parser()
        # self.parser.load(par_model_path)
        #
        # # 语义角色标注模型目录路径，模型目录为`srl`
        # self.labeller = SementicRoleLabeller()  # 初始化实例
        # self.labeller.load(srl_model_path)  # 加载模型

        # 加载word2vec 模型
        pass

    @pysnooper.snoop()
    def release_all_model(self):
        """释放模型"""
        self.segmentor.release()
        self.postager.release()
        self.recognizer.release()
        self.parser.release()
        # word2vec 模型的释放
        pass

    # 分句
    @pysnooper.snoop()
    def split_sentences(self, string):
        sents = SentenceSplitter.split(string)
        sentences = [s for s in sents if len(s) != 0]
        return sentences

    def jieba_word_cut(self, string):
        string = re.findall(
            '[\d|\w|\u3002 |\uff1f |\uff01 |\uff0c |\u3001 |\uff1b |\uff1a |\u201c |\u201d |\u2018 |\u2019 |\uff08 |\uff09 |\u300a |\u300b |\u3008 |\u3009 |\u3010 |\u3011 |\u300e |\u300f |\u300c |\u300d |\ufe43 |\ufe44 |\u3014 |\u3015 |\u2026 |\u2014 |\uff5e |\ufe4f |\uffe5]+',
            string)
        string = ' '.join(string)

        return ' '.join(jieba.cut(string))

    # 分词
    @pysnooper.snoop()
    def split_words(self, sentences):
        sents = [self.jieba_word_cut(s) for s in sentences]
        return sents

    # 词性分析
    @pysnooper.snoop()
    def get_word_pos(self, sents):
        postags = [self.postager.postag(words.split()) for words in sents]
        postags = [list(w) for w in postags]
        return postags

    # 依存句法分析
    @pysnooper.snoop()
    def dependency_parsing(self, sents, postags, said):

        contents = []
        for index in range(len(sents)):
            wo = sents[index].split()
            po = postags[index]

            netags = self.recognizer.recognize(wo, po)  # 命名实体识别
            netags = list(netags)
            # print(netags)
            if ('S-Nh' not in netags) and ('S-Ni' not in netags) and (
                    'S-Ns' not in netags):  # 人名、机构名、地名  当人名、机构名、地名在该句中则进行依存句法分析
                continue

            arcs = self.parser.parse(wo, po)

            arcs = [(arc.head, arc.relation) for arc in arcs]
            # print(arcs)  #[(2, 'SBV'), (0, 'HED'), (5, 'SBV'), (5, 'ADV'), (2, 'VOB')]
            arcs = [(i, arc) for i, arc in enumerate(arcs) if arc[1] == 'SBV']  # SBV 主谓关系 找出主谓关系的句子
            # print(arcs)  #[(0, (2, 'SBV')), (2, (5, 'SBV'))]
            for arc in arcs:
                verb = arc[1][0]  # 2  5
                subject = arc[0]  # 0  1
                if wo[verb - 1] not in said:  # 如果wo[verb - 1]这个所对应的词语  在已建词表said中，则打印出来
                    continue
                # print(wo[subject],wo[verb - 1],''.join(wo[verb:]))
                contents.append((wo[subject], wo[verb - 1], ''.join(wo[verb:])))  # 依次为人物、"说"的近义词、文本

        return contents

    @pysnooper.snoop()
    def get_sentences_json_result(self, string):
        """
        对输入的句子进行SBV提取
        :param string:
        :return: list of dict [{}]
        """

        sentences = self.split_sentences(string)  # 分句
        sents = self.split_words(sentences)  # 分词
        postags = self.get_word_pos(sents)  # 词性分析
        contents = self.dependency_parsing(sents, postags, txt_said)  # 依存句法分析

        # 拼装json结果
        contents_dict = []
        for ones in enumerate(contents):
            # json 字段
            result = {'name': ones[1][0], 'trigger': ones[1][1], 'content': ones[1][2]}
            contents_dict.append(result)
        return contents_dict


ltp_manager = LtpModel(LTP_DATA_DIR)

if __name__ == '__main__':
    ltp_manager = LtpModel(LTP_DATA_DIR)
    # ltp_manager.release_all_model()
    string = """国台办表示中国必然统一。会尽最大努力争取和平统一，但绝不承诺放弃使用武力。
    昨天想睡觉"""
    print(ltp_manager.get_sentences_json_result(string))
