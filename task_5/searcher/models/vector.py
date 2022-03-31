from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer
import numpy as np
import re
from scipy import spatial

from models.const import STOPWORDS, pattern

indexes = {}


class Vector:
    def __init__(self):
        self.lemmas, self.matrix = self.get_inverted_index()
        with open(r'/home/emin/inf-search/task_1/files/index.txt') as index:
            items = index.readlines()
            for item in items:
                key, value = item.split(' ')
                indexes[key] = value
        self.morph = MorphAnalyzer()

    def get_inverted_index(self):
        with open(r'/home/emin/inf-search/task_3/inverted_index.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()

        l_list = list()
        array_m = [[0] * 500 for _ in range(len(lines))]
        for i, l in enumerate(lines):
            l = re.sub('\n', '', l)
            lemma = l.split(' ')[0]
            l_list.append(lemma)
            pages = l.split(' ')[1].split(' ')
            for p in pages:
                array_m[i][int(p) - 1] = 1

        return l_list, np.array(array_m).transpose()

    def vectorize(self, query):
        tokens = word_tokenize(query)
        req_tokens = [line_token.lower() for line_token in tokens]
        tokens_del = [item for item in req_tokens if item not in STOPWORDS and pattern.match(item)]

        parse_token = [self.morph.parse(token)[0].normal_form for token in tokens_del]
        vector = [0] * len(self.lemmas)
        for i in parse_token:
            if i in self.lemmas:
                vector[self.lemmas.index(i)] = 1

        return vector

    def search(self, query):
        vector = self.vectorize(query)

        query_m = dict()
        for i, j in enumerate(self.matrix):
            if max(j) == 1:
                query_m[i + 1] = 1 - spatial.distance.cosine(vector, j)
            else:
                query_m[i + 1] = 0.0

        query_s = sorted(query_m.items(), key=lambda x: x[1], reverse=True)
        query_indexes = [(indexes.get(str(doc[0])), doc) for doc in query_s]
        return query_indexes
