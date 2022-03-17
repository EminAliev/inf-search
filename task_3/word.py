"""
Класс подсчета слов
"""


class Count:
    def __init__(self):
        self.texts = []
        self.count = 0

    def get_text_result(self, texts, count):
        self.texts.append(texts)
        self.count += count
