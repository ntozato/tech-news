import requests
import time
from parsel import Selector
from tech_news.database import create_news


def shares_count_repair(selector):
    shares_count = selector.css(
        "div.tec--toolbar__item"
        "::text").get()

    if shares_count:
        shares_count = shares_count.split(" ")[1]
        shares_count = int(shares_count)
    else:
        shares_count = 0
    return shares_count


def writer_repair(selector):
    writer = selector.css("div.tec--author__info ::text").get()

    if writer is None:
        writer = selector.css("div.z--font-bold a::text").get()
    if writer:
        writer = writer.strip()
    return writer


# Requisito 1
def fetch(url):
    try:
        time.sleep(1)
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
    except requests.Timeout:
        return None
    else:
        return None


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(html_content)
    result = selector.css("h3.tec--card__title a::attr(href)").getall()
    if not result:
        return []
    return result


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    result = selector.css(
        "#js-main > div > div > div.z--col.z--w-2-3 >"
        "div.tec--list.tec--list--lg > a::attr(href)").get()
    return result


# Requisito 4

# https://stackoverflow.com/questions/12453580/how-to-concatenate-items-in-a-list-to-a-single-string
# https://www.jcchouinard.com/web-scraping-with-python-and-requests-html/
def scrape_noticia(html_content):
    selector = Selector(html_content)

    url = selector.xpath("//link[@rel='canonical']/@href").get()

    title = selector.css("h1.tec--article__header__title ::text").get()

    timestamp = selector.css("#js-article-date ::attr(datetime)").get()

    writer = writer_repair(selector)

    shares_count = shares_count_repair(selector)

    comments_count = selector.css("#js-comments-btn ::attr(data-count)").get()

    summary = "".join(
        selector.css("div.tec--article__body > p:nth-child(1) ::text").getall()
    )

    sources_list = selector.css(
        "div.z--mb-16 div a::text").getall()

    sources = []

    for item in sources_list:
        sources.append(item.strip())

    categories_list = selector.css("#js-categories a::text").getall()

    categories = []

    for item in categories_list:
        categories.append(item.strip())

    return {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": int(comments_count),
        "summary": summary,
        "sources": sources,
        "categories": categories,
    }


# Requisito 5
def get_tech_news(amount):
    URL_BASE = "https://www.tecmundo.com.br/novidades"
    main_html_content = fetch(URL_BASE)
    news = scrape_novidades(main_html_content)
    selected_news = []

    while len(news) < amount:
        next_page_url = scrape_next_page_link(main_html_content)
        main_html_content = fetch(next_page_url)
        novidades = scrape_novidades(main_html_content)

        for link in novidades:
            news.append(link)

    # https://www.delftstack.com/pt/howto/python/python-find-index-of-value-in-array/
    for link in news:
        if news.index(link) < amount:
            new_html_content = fetch(link)
            noticia = scrape_noticia(new_html_content)
            selected_news.append(noticia)

    create_news(selected_news)
    return selected_news


if __name__ == "__main__":
    main_page_html_content = fetch("https://www.tecmundo.com.br/novidades")
    new_page_html_content = fetch(
        "https://www.tecmundo.com.br/minha-serie/215168-10-"
        "viloes-animes-extremamente-inteligentes.htm")
    teste = scrape_noticia(new_page_html_content)
    print(teste['timestamp'])
