import requests
import bs4

BASE_URL = 'https://habr.com'
url = 'https://habr.com/ru/all/'
KEYWORDS = {'Дизайн', 'Фото', 'Web', 'Python'}

def site_request(URL):
    response = requests.get(URL)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    return soup

def main():
    soup = site_request(url)
    articles = soup.find_all('article')
    for article in articles:
        hubs = article.find_all(class_='tm-article-snippet__hubs-item-link')
        hubs = set(hub.find('span').text for hub in hubs)
        # Поиск совпадений ключевых слов и хабов
        if KEYWORDS & hubs:
            date = article.find('time').attrs['title'].split(',')[0]
            heading = article.find('h2').text
            href = article.find(class_='tm-article-snippet__title-link').attrs['href']
            link_article = BASE_URL + href
            print(f"{date} - {heading} - {link_article}")
        # Поиск совпадений в тексте статьи
        else:
            n = 0
            href = article.find(class_='tm-article-snippet__title-link').attrs['href']
            link_article = BASE_URL + href
            soup_Article = site_request(link_article)
            paragraphs = soup_Article.find_all('p')
            for KEYWORD in KEYWORDS:
                for paragraph in paragraphs:
                    if paragraph.text.lower().find(KEYWORD.lower()) > -1:
                        n += 1
                        break
            if n > 0:
                date = soup_Article.find('time').attrs['title'].split(',')[0]
                heading = soup_Article.find('h1').text
                print(f"{date} - {heading} - {link_article}")

if __name__ == "__main__":
    main()