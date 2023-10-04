from typing import List

from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import MathpixPDFLoader
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import PyPDFLoader
from logger import logger as log

logger = log.get_logger("pdf_reader")

# text splitter for chatGPT 3.5
text_splitter = TokenTextSplitter(
    chunk_size=1024, chunk_overlap=32, model_name="gpt-3.5-turbo"
)


def get_splitted_text(text: str) -> List[str]:
    return text_splitter.split_text(text)


def read_pdf(pdf_path: str) -> List[str]:
    doc = PyPDFLoader(pdf_path).load()
    # logger.info(doc[0].page_content)
    chunks = []
    for page in doc:
        chunks += text_splitter.split_text(page.page_content)
    return chunks


if __name__ == "__main__":
    chunks = read_pdf(
        "/home/kave/work/pdf2menu/menus/OM_MenuKaart_Juli_2023_Online_NL.pdf"
    )
    logger.info(chunks)
