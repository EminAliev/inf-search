import zipfile
import re
import functools
import pymorphy2
import nltk
from bs4 import BeautifulSoup

from word import Count


class BooleanSearch:
    def __init__(self):
        self.path_pages = '/home/emin/inf-search/task_1/files/pages.zip'
        self.path_lemmas = '/home/emin/inf-search/task_2/files/lemmas.txt'

    def get_lemma(self, word):
        """
        Получение леммы
        :param word:
        :return:
        """
        morph_parse = pymorphy2.MorphAnalyzer().parse(word)[0]
        if morph_parse.normalized.is_known:
            normal_form = morph_parse.normal_form
        else:
            normal_form = word.lower()
        return normal_form

    def word_find_index(self, words_index_mapping):
        """
        Нахождение слов по леммам в html
        :param words_index_mapping:
        :return:
        """
        files = zipfile.ZipFile(self.path_pages, 'r')
        index = dict()
        for file in files.filelist:
            html = files.open(file.filename)
            content = BeautifulSoup(html, features="html.parser").get_text()
            list_word = list(nltk.wordpunct_tokenize(content))
            words = set()
            for word in list_word:
                lemma = self.get_lemma(word)
                if lemma in words_index_mapping.keys() and lemma not in words:
                    words.add(lemma)
                    word_special = words_index_mapping[lemma]
                    count = 0
                    for similar_word in word_special:
                        count += list_word.count(similar_word)
                    if lemma not in index.keys():
                        index[lemma] = Count()
                    index[lemma].get_text_result(file.filename, count)
        return dict(sorted(index.items()))

    def create_inverted_index(self):
        """
        Создание индекса
        :return:
        """
        file = open(self.path_lemmas, "r")
        lines = file.readlines()
        words_index_mapping = dict()
        for line in lines:
            k = None
            words = re.split('\s+', line)
            for i in range(len(words) - 1):
                if i == 0:
                    k = words[i]
                    words_index_mapping[k] = []
                else:
                    words_index_mapping[k].append(words[i])
        index = self.word_find_index(words_index_mapping)
        index_sort = dict(
            sorted(index.items(), key=functools.cmp_to_key(x[1].general_count - y[1].general_count), reverse=True))
        file = open("inverted_index.txt", "w")
        for word, inf in index_sort.items():
            file_field = word + " "
            for doc in inf.documents:
                file_field += " " + str(doc)
            file_field += "\n"
            file.write(file_field)
        file.close()

    def inverted_index_open(self):
        """
        Открытие файла с индексом
        :return:
        """
        file = open("inverted_index.txt", "r")
        lines = file.readlines()
        words_index_mapping = dict()
        for line in lines:
            words = re.split('\s+', line)
            k = words[0]
            if not k in words_index_mapping.keys():
                words_index_mapping[k] = set()
            for i in range(1, len(words) - 1):
                words_index_mapping[k].add(words[i])
        return words_index_mapping

    def search(self, index, word):
        words = re.split('\s+', word)
        content_page = set()
        lemma_token = set(map(lambda x: self.get_lemma(x), words))
        for word in lemma_token:
            content_page = content_page | index[word]


s = BooleanSearch()
s.create_inverted_index()
s.search(s.inverted_index_open(), 'футбол')
