from tech_news.database import find_news
from tech_news.database import db
from datetime import datetime
import re


# Requisito 6
# https://stackoverflow.com/questions/4976278/python-mongodb-regex-ignore-case/4976333

def search_by_title(title):
    news_list = list(db.news.find({"title": re.compile(title, re.IGNORECASE)}))
    news = []

    for item in news_list:
        news.append((item["title"], item["url"]))

    return news


# "https://www.datacamp.com/community/tutorials/converting-strings-datetime-"
# "objects?utm_source=adwords_ppc&utm_medium=cpc&utm_campaignid=14989519638&"
# "utm_adgroupid=127836677279&utm_device=c&utm_keyword=&utm_matchtype=&utm_network"
# "=g&utm_adpostion=&utm_creative=278443377095&utm_targetid=dsa-"
# "429603003980&utm_loc_interest_ms=&utm_loc_physical_ms"
# "=1031430&gclid=CjwKCAiA55mPBhBOEiwANmzoQjQUjh1y9sp55Noh"
# "hbOdCEhDoTIKYMyJfrF8NA6r0s6bjinR3ujeOxoCrqEQAvD_BwE"

# Requisito 7
def search_by_date(date):

    try:
        datetime.strptime(date, "%Y-%m-%d")
        news_list = find_news()
        result = []

        for item in news_list:
            if item['timestamp'][:10] == date:
                result.append((item['title'], item['url']))

        return result

    except ValueError:
        raise ValueError('Data inválida')


# Requisito 8
def search_by_source(source):
    news_list = list(db.news.find({"sources": re.compile(source, re.IGNORECASE)}))
    news = []

    for item in news_list:
        news.append((item["title"], item["url"]))

    return news


# Requisito 9
def search_by_category(category):
    news_list = list(db.news.find({"categories": re.compile(category, re.IGNORECASE)}))
    news = []

    for item in news_list:
        news.append((item["title"], item["url"]))

    return news


if __name__ == "__main__":
    teste = search_by_source("teste")
    print(teste)
