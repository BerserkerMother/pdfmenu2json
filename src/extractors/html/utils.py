import time
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4.element import Comment

from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter

from logger import logger as log

logger = log.get_logger("HTML")

# text splitter for chatGPT 3.5
text_splitter = TokenTextSplitter(
    chunk_size=1024, chunk_overlap=32, model_name="gpt-3.5-turbo"
)


def get_html(link: str, time_to_sleep: int = 1) -> str:
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # for Chrome >= 109
    
    # start web browser
    browser = webdriver.Chrome(options=chrome_options)

    # get source code
    browser.get(link)

    html = browser.page_source
    time.sleep(time_to_sleep)

    # close web browser
    browser.close()

    # convert to bs4
    soup = BeautifulSoup(html, "html.parser")

    return soup


def get_chunks(link: str, time_to_sleep: int = 1) -> List[str]:
    soup = get_html(link=link, time_to_sleep=time_to_sleep)
    html_str = text_from_html(soup=soup)
    chunks = text_splitter.split_text(html_str.strip())
    return chunks


def tag_visible(element):
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
    ]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(soup):
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)
    return "\n".join(t.strip() for t in visible_texts)


if __name__ == "__main__":
    get_html(link="https://www.gysutrecht.nl/en/menu")
