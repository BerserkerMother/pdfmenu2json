import os
from typing import List

from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import MathpixPDFLoader
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.document_loaders import PyPDFLoader
from logger import logger as log

logger = log.get_logger("PDF")

# text splitter for chatGPT 3.5
text_splitter = TokenTextSplitter(
    chunk_size=1024, chunk_overlap=32, model_name="gpt-3.5-turbo"
)


def save_pdf_menu(pdf_menu) -> str:
    """saves pdf file locally

    returns: path to pdf file"""
    file_path = pdf_menu.filename
    pdf_menu.save(file_path)
    return file_path


def get_chunks(pdf_menu):
    file_path = save_pdf_menu(pdf_menu=pdf_menu)
    chunks = read_pdf(pdf_path=file_path)
    os.remove(file_path)
    return chunks


def get_splitted_text(text: str) -> List[str]:
    return text_splitter.split_text(text)


def read_pdf(pdf_path: str) -> List[str]:
    doc = PyPDFLoader(pdf_path).load()
    chunks = []
    for page in doc:
        chunks += text_splitter.split_text(page.page_content)
    return chunks
