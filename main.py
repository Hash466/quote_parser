import asyncio
import sys

from bs4 import BeautifulSoup
from httpx import AsyncClient

from core.config import BASE_URL
from core.logger import get_logger
from core.schema import Author, QuoteArr, QuoteItem
from core.utils import save_json_async, text_clean


logger = get_logger(__name__)

about_author = {}


async def fetch(url: str) -> str:
    async with AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)
        logger.debug("Страница с адресом: %s успешно загружена", url)
        return response


async def fetch_about_author(url: str) -> str:
    if about_author.get(url):
        logger.debug("Информация об авторе ранее уже была загружена")
        return about_author[url]

    logger.debug("Загружаю страницу с данными об авторе")
    full_url = BASE_URL + url
    response = await fetch(full_url)

    logger.debug("Определяю элементы разметки на странице данных об авторе")
    soup = BeautifulSoup(response, 'html.parser')

    logger.debug("Собираю набор данных автора")
    author_name = soup.find("h3", class_="author-title")
    author_was_born_1 = soup.find("span", class_="author-born-date")
    author_was_born_2 = soup.find("span", class_="author-born-location")
    author_was_born = " ".join(
        [author_was_born_1.text, author_was_born_2.text]
    )
    author_description = soup.find("div", class_="author-description")

    logger.debug("Создаю новый объект класса Author")
    author = Author(
        name=author_name.text,
        was_born=author_was_born,
        description=text_clean(author_description.text)
    )

    logger.debug("Добавляю запись о новом авторе в массив about_author")
    about_author[url] = author

    return author


async def process_markup(markup: str, quote_arr: QuoteArr):
    soup = BeautifulSoup(markup, 'html.parser')

    logger.debug("Определяю элементы разметки на странице с цитатами")
    elements = soup.find_all(
        "div", class_="quote", itemtype="http://schema.org/CreativeWork"
    )

    if not quote_arr.get_len():
        logger.debug("Получаю топ тегов в порядке убывания популярности")
        tags_div = soup.find("div", class_="col-md-4 tags-box")
        tags = tags_div.find_all("a", class_="tag")
        logger.info("Добавляю топ тегов в массив цитат")
        for tag in tags:
            quote_arr.add_top_tag(tag.text)

    logger.debug("Начинаю итерацию по найденным элементам")
    for element in elements:
        logger.debug("Собираю набор данных цитаты")
        quote_txt = element.select_one(
            "span", class_="text", itemprop="text"
        )
        quote_by = element.select_one(
            "small", class_="author", itemprop="author"
        )
        quote_tags = [tag.text for tag in element.select("a.tag")]
        author_link = element.select_one("a:not(.tag)")

        logger.debug("Получаю сведения об авторе")
        author = await fetch_about_author(author_link.get("href"))

        logger.debug("Создаю новый объект цитаты")
        quote = QuoteItem(
            tags=quote_tags,
            by=quote_by.text,
            text=quote_txt.text,
            about_author=author.fetch_object()
        )

        logger.info("Добавляю новую цитату: < %s > в массив", quote.__str__())
        quote_arr.add_quote(quote)

    logger.debug("Ищу ссылку на следующую страницу")
    next = soup.find("li", class_="next")
    if next:
        logger.info("Найдена ссылка на следующую страницу")
        next_link = soup.find('li', class_='next').find('a')
        return next_link.get("href")

    logger.info("Ссылка на следующую страницу отсутствует")
    return None


async def run_pars(url: str) -> None:
    logger.info("Начинаю парсинг %s", url)
    logger.debug("Инициализирую пустой массив цитат")
    quote_arr = QuoteArr()

    logger.debug("Загружаю целевой URL")
    response = await fetch(url)
    logger.debug("Начинаю анализ полученной разметки")
    next_page = await process_markup(markup=response, quote_arr=quote_arr)

    while next_page:
        logger.debug("Загружаю целевой URL")
        response = await fetch(BASE_URL+next_page)
        logger.debug("Начинаю анализ полученной разметки")
        next_page = await process_markup(markup=response, quote_arr=quote_arr)
    logger.info("Все данные собраны")

    await save_json_async(quote_arr.fetch_object())
    logger.info("Все данные собраны и сохранены в результирующий файл")


async def main() -> None:
    task_parsing = asyncio.create_task(run_pars(BASE_URL))
    await asyncio.gather(task_parsing,)


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        raise sys.exit(0)
