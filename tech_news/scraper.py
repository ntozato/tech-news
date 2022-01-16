import requests
import time
from parsel import Selector


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
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""


if __name__ == "__main__":
    main_page_html_content = fetch("https://www.tecmundo.com.br/novidades")
    teste = scrape_next_page_link(main_page_html_content)
    print(teste)
