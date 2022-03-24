import os
from collections import Counter
from math import log10

import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

NLTK_PACKAGES = ['tokenizers/punkt', 'corpora/stopwords', 'corpora/wordnet', 'corpora/omw-1.4']


class TfIdf:

    def tokenize(self, page):
        tokens = nltk.word_tokenize(page)
        low_tokens = [token.lower() for token in tokens if token.isalpha()]
        return [token for token in low_tokens if token not in stopwords.words('english')]

    def lemmatize(self, tokens):
        lemmatizer = WordNetLemmatizer()
        dict_lemma = {}
        for token in tokens:
            lemma = lemmatizer.lemmatize(token)
            lemma_dict_map = dict_lemma.get(lemma, [])
            lemma_dict_map.append(token)
            dict_lemma[lemma] = lemma_dict_map
        return dict_lemma

    def get_tf(self, pages, counters, word_in):
        pages_tf = []
        for page, counter in zip(pages, counters):
            count = len(page)
            tf = {}
            for word in word_in:
                tf[word] = counter[word] / count
            pages_tf.append(tf)
        return pages_tf

    def get_idf(self, count, counter, word_in):
        counters = dict.fromkeys(word_in, 0)
        for p_counter in counter:
            for word in word_in:
                if p_counter[word] != 0:
                    counters[word] += 1

        idf = {}
        for word in word_in:
            idf[word] = log10(count / counters[word])
        return idf

    def get_tf_idf(self, tf, idf, word_in):
        idf_tf = []
        for tf_count in tf:
            idf_tf_dict = {}
            for word in word_in:
                idf_tf_dict[word] = tf_count[word] * idf[word]
            idf_tf.append(idf_tf_dict)
        return idf_tf

    def write_tf_idf(self, pages_tf, idf, pages_tf_idf, corpus, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)

        i = 0
        for page_tf, page_tf_idf in zip(pages_tf, pages_tf_idf):
            i += 1
            with open(f'{directory}/page_{i}.txt', 'w', encoding='utf-8') as file:
                for word in corpus:
                    file.write(f'{word} {page_tf[word]} {idf[word]} {page_tf_idf[word]}\n')
