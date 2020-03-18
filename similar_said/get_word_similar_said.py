#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@IDE    ：PyCharm
@Author ：LuckyHuibo
@Date   ：2019/8/28 13:15
@Desc   ：
1、利用word2vec（模型是预训练好的）跟广度优先搜索算法获取跟“说”有关的词，保存到../data/words.txt
2、加载数据进行查看
=================================================='''
from gensim.models import Word2Vec
from collections import defaultdict
from config.file_path import said_path
import os


def get_related_words(initial_words, model):
    """
    @initial_words
    @model
    """

    unseen = initial_words

    seen = defaultdict(int)

    max_size = 500

    while unseen and len(seen) < max_size:
        if len(seen) % 50 == 0:
            print('seen length : {}'.format(len(seen)))
        node = unseen.pop(0)

        new_expanding = [w for w, s in model.most_similar(node, topn=20)]

        unseen += new_expanding

        seen[node] += 1
    return seen


def get_words_said(model_path):
    model = Word2Vec.load(model_path)
    related_words = get_related_words(['说', '表示', '认为'], model)
    related_words = sorted(related_words.items(), key=lambda x: x[1], reverse=True)
    print(related_words)
    said = [i[0] for i in related_words if i[1] >= 1]

    return said


def save_said(wv_model_path, save_path):
    said = get_words_said(wv_model_path)
    string = '|'.join(said)
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(string)
        return True
    except:
        return False


def load_said(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            string = f.readlines()
            string = string[0].split('|')
            return string


txt_path = os.path.join(said_path, "similar_said.txt")
txt_said = load_said(txt_path)

if __name__ == '__main__':
    wv_model_path = "../data/zhwiki_news.word2vec"
    result = save_said(wv_model_path=wv_model_path, save_path="similar_said.txt")
    if result:
        string = load_said("../data/words.txt")
        print(string)
    model = Word2Vec.load(wv_model_path)
    said = model['说']
    print(said)
