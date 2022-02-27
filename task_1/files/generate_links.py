import requests, os


class Generator:
    def __init__(self):
        self.search_query = 'спорт'
        self.max_requests = 6

    def generate(self):

        links = open("input.txt", "a", encoding="utf-8")

        for i in range(self.max_requests):
            request = requests.get(
                'https://www.liveinternet.ru/rating/today.tsv?;search=' + self.search_query + ';page=' + str(i))
            data = request.text.split("\n")
            for row in data[1:30]:
                url = row.split("\t")[1].replace("/", "")
                if url.find('ua'):
                    continue
                else:
                    print(url + '\n', end='')
                    links.write(url + "\n")
        links.close()

