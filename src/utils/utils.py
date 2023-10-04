import os
import re
from typing import Dict, List

from langchain import PromptTemplate
from langchain.chains import SequentialChain, LLMChain
from langchain.llms import OpenAI

from langchain.output_parsers import CommaSeparatedListOutputParser

from logger import logger as log
from .pdf_reader import read_pdf

logger = log.get_logger("utils")


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


def llm_to_json(menu_dict: Dict, items_unstructured) -> Dict:
    """Adds llm menu item findings to a dictionary for api"""
    logger.info(items_unstructured)
    for item in items_unstructured.split(";"):
        food_price = item.split(":")
        # logger.info(food_price)
        if len(food_price) == 2:
            name = re.sub(r"\n|\t", "", food_price[0])
            price = format_price(food_price[1])
            price = to_float(price)
            if not price:
                continue
            # logger.info(name)
            # logger.info(price)
            menu_dict["menu"].append({"name": name.lower(), "price": price})
        # logger.info("_" * 100)
    return menu_dict


def get_parsing_chain():
    llm = OpenAI(temperature=0.0)

    # extracting food from menu
    fi_food = (
        "your response should be a list of comma separated values, eg: `foo, bar, baz`"
    )
    food_template = (
        "You are given a menu of a restaurant foods. The menu consists of foods with their prices and their ingridents."
        "List only the food items in the menu.\n{document}.\n{fi_food}"
    )
    prompt_food = PromptTemplate(
        template=food_template,
        input_variables=["document"],
        partial_variables={"fi_food": fi_food},
        # output_parser=CommaSeparatedListOutputParser(),
    )
    food_chain = LLMChain(llm=llm, prompt=prompt_food, output_key="foods", verbose=True)

    fi_price = "your response should be a list of food and their prices separated by ; , eg: `foo: 20$; bar: 10$; baz: 43$`"
    price_template = (
        "Your task is to find prices for each food in a restaurant menu. Some foods may be grouoped together"
        " and share the same price."
        "Extract the price for foods: {foods} from the restaurant menu\nmenu:\n{document}.\n{fi_price}."
    )
    prompt_price = PromptTemplate(
        template=price_template,
        input_variables=["foods", "document"],
        partial_variables={"fi_price": fi_price},
        # output_parser=CommaSeparatedListOutputParser(),
    )
    price_chain = LLMChain(
        llm=llm, prompt=prompt_price, output_key="menu", verbose=True
    )

    language_chain = SequentialChain(
        chains=[food_chain, price_chain],
        input_variables=["document"],
        output_variables=["menu"],
        verbose=True,
    )

    return language_chain


def to_float(num: str) -> float:
    """helper function to check if str can be converted to float"""
    try:
        return float(num)
    except Exception as e:
        logger.error(f"Error while trying to convert to float{e}")
        return False


def format_price(price: str) -> str:
    price = re.sub(r",", ".", price)
    price = re.sub(r"\n|\t|\$|€", "", price)
    if price.endswith("."):
        price = price[:-1]
    return price
