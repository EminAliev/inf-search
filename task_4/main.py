import os
from collections import Counter

from nltk import WordNetLemmatizer

from tf_idf import TfIdf

if __name__ == '__main__':
    tf_handler = TfIdf()
    lemmatizer = WordNetLemmatizer()

    pages = []
    counters = []
    for file in sorted(os.listdir('/home/emin/inf-search/task_1/files/pages'), key=len):
        with open('/home/emin/inf-search/task_1/files/pages'f'/{file}', 'r', encoding='utf-8') as page:
            tokens = tf_handler.tokenize(page.read())
            pages.append(tokens)
            counters.append(Counter(tokens))

    tokens = set()
    with open('/home/emin/inf-search/task_2/files/tokens.txt', encoding="utf-8") as file:
        for line in file.readlines():
            tokens.add(line.strip())

    tf_pages_token = tf_handler.get_tf(pages, counters, tokens)
    idf_token = tf_handler.get_idf(len(pages), counters, tokens)
    tf_idf_token = tf_handler.get_tf_idf(tf_pages_token, idf_token, tokens)

    i = 0
    for page_tf, page_tf_idf in zip(tf_pages_token, tf_idf_token):
        i += 1
        with open('tokens'f'/page_{i}.txt', 'w', encoding='utf-8') as file:
            for word in tokens:
                file.write(f'{word} {page_tf[word]} {idf_token[word]} {page_tf_idf[word]}\n')

    lemmas = set()
    with open('/home/emin/inf-search/task_2/files/lemmas.txt', encoding='utf-8') as lemmas_file:
        for line in lemmas_file.readlines():
            values = line.strip().split(' ')
            lemmas.add(values[0].replace(':', ''))

    counters_lemmas = []
    for page_token in pages:
        lemma_page = list(map(lambda token: lemmatizer.lemmatize(token), page_token))
        counters_lemmas.append(Counter(lemma_page))

    tf_lemma = tf_handler.get_tf(pages, counters_lemmas, lemmas)
    idf_lemma = tf_handler.get_idf(len(pages), counters_lemmas, lemmas)
    tf_idf_lemma = tf_handler.get_tf_idf(tf_lemma, idf_lemma, lemmas)

    i = 0
    for page_tf, page_tf_idf in zip(tf_lemma, tf_idf_lemma):
        i += 1
        with open('lemmas'f'/page_{i}.txt', 'w', encoding='utf-8') as file:
            for word in lemmas:
                file.write(f'{word} {page_tf[word]} {idf_lemma[word]} {page_tf_idf[word]}\n')
