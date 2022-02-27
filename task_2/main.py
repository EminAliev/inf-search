import re
import string
from os import listdir
from os.path import isfile, join

import nltk
import pymorphy2
from bs4 import BeautifulSoup
from nltk.corpus import stopwords


class Tokenizer:
    def __init__(self):
        self.files_path = 'files/pages'
        self.morph = pymorphy2.MorphAnalyzer()
        self.stop_words = stopwords.words('russian')

    def tokenizer(self, text):
        content = BeautifulSoup(text).get_text()
        tokenizer_result_list = list(nltk.wordpunct_tokenize(content))
        tokenizer_result_list = [i for i in tokenizer_result_list if all(not j in string.punctuation for j in i)]
        tokenizer_result_list = list(filter(self.remove_incorrect, tokenizer_result_list))
        return tokenizer_result_list

    def remove_incorrect(self, word):
        letters = re.compile(r'^[а-яА-Я]{2,}$')
        numbers = re.compile(r'^[0-9]+$')
        result = bool(numbers.match(word)) or not bool(letters.match(word)) or bool(word.lower() in self.stop_words)
        return not result

    def lemmatizer(self, result):
        lem_dict = dict()
        for word in result:
            morph_parse_word = self.morph.parse(word)[0]
            if morph_parse_word.normalized.is_known:
                normal_form = morph_parse_word.normal_form
            else:
                normal_form = word.lower()
            if not normal_form in lem_dict:
                lem_dict[normal_form] = []
            lem_dict[normal_form].append(word)
        return lem_dict

    def handler(self):
        files = [f for f in listdir(self.files_path) if isfile(join(self.files_path, f))]
        files_len = len(files)
        token_result = set()
        for i in range(files_len):
            file_name = files[i]
            print('Processing site ' + str(i) + '/' + str(files_len) + '. ' + file_name)
            file = open(self.files_path + '/' + file_name, "r", encoding="utf-8")
            token_file = set(self.tokenizer(file))
            token_result = token_result | token_file
            print(file_name, "done")
        tokens = open("tokens.txt", "a")
        for word in token_result:
            tokens.write("%s\n" % word)
        tokens.close()
        lem_result = self.lemmatizer(token_result)
        lemmas = open("lemmas.txt", "a")
        for lemma, tokens in lem_result.items():
            words = lemma + " "
            for token in tokens:
                words += token + " "
            words += "\n"
            lemmas.write(words)
        lemmas.close()


if __name__ == '__main__':
    t = Tokenizer()
    t.handler()

