import os
import requests


class Crawler:
    def __init__(self):
        self.folder_name = 'files/pages'
        self.input_file = 'files/input.txt'

    def handler(self):
        """
        Выкачка html страниц
        :return:
        """
        os.mkdir(self.folder_name)

        urls = [line.rstrip('\n') for line in open(self.input_file)]
        urls_set = set(urls)
        unique_urls = list(urls_set)

        index_file = open("files/index.txt", "a", encoding="utf-8")
        iterator = 0

        for url in unique_urls:
            try:
                req_url = "http://" + url
                text = self.get_request(req_url)
                if text is None:
                    continue
            except Exception as error:
                print(url + " Error " + format(error))
            else:
                iterator += 1
                print(str(iterator) + '. ' + url + " ... ", end='')

                filename = self.folder_name + '/' + 'выкачка_' + url + '_' + str(iterator) + ".html"
                page = open(filename, "a", encoding="utf-8")
                page.write(text)
                page.close()
                index_file.write(str(iterator) + ' ' + url + "\n")
        index_file.close()

    def get_request(self, url: str):
        """
        Получение текста страницы
        :param url: адрес страницы
        :return: текст страницы
        """
        request = requests.get(url)
        request.encoding = request.apparent_encoding
        if request.status_code == 200:
            return request.text
        else:
            return None


if __name__ == '__main__':
    c = Crawler()
    c.handler()
