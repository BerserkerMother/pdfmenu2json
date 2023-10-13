import os
import re
from typing import Dict, List

import google.cloud.logging

from logger import logger as log
from logger import LoggingExtras


logger = log.get_logger("utils")

client = google.cloud.logging.Client()
client.setup_logging()


def extract_menu_items(chain_price, chain_category, chunks: List[str]) -> Dict:
    menu_items = {"menu": []}
    foods_name = []  # for category later
    for chunk in chunks:
        # log.info(chunk)
        items_unstructured = chain_price.run(chunk)
        menu_items, foods_name = add_price_to_json(
            menu_dict=menu_items,
            foods_name=foods_name,
            items_unstructured=items_unstructured,
        )
    food_categories = {}
    for i in range(0, len(foods_name), 25):
        foods_slice = foods_name[i : i + 25]
        foods_slice = ", ".join(foods_slice)
        category_llm_out = chain_category.run(foods_slice)
        format_category_to_dict(category_llm_out, food_categories)
    add_category_to_json(menu_items, food_categories)
    return menu_items


def add_price_to_json(
    menu_dict: Dict, foods_name: List, items_unstructured
) -> [Dict, List[str]]:
    """Adds llm menu item findings to a dictionary for api"""
    for item_price in items_unstructured.split(";"):
        logger.info(item_price, extra={"json_fields": LoggingExtras.Success})
        food_price = item_price.split(":")
        if len(food_price) == 2:
            name = re.sub(r"\n|\t", "", food_price[0])
            name = name.lower().strip()
            price = format_price(food_price[1])
            price = to_float(price)
            if not price:
                logger.warning(
                    item_price, extra={"json_fields": LoggingExtras.PriceError}
                )
                price = 0
            menu_dict["menu"].append({"name": name, "price": price, "category": ""})
            foods_name.append(name)
        else:
            logger.warning(item_price, extra={"json_fields": LoggingExtras.ItemError})
    return menu_dict, foods_name


def format_category_to_dict(llm_out: str, food_categories: Dict) -> Dict:
    for item in llm_out.split(";"):
        food_category = item.split(":")
        if len(food_category) == 2:
            name = re.sub(r"\n|\t", "", food_category[0])
            name = name.lower().strip()
            category = food_category[1].strip().lower()
            food_categories[name] = category
    return food_categories


def add_category_to_json(menu_dict: Dict, food_categories: Dict) -> Dict:
    for item in menu_dict["menu"]:
        try:
            category = food_categories[item["name"]]
            item["category"] = category
        except Exception as e:
            logger.warning(f"COULDN'T FIND CATEGORY for {item['name']}")
    return menu_dict


def to_float(num: str) -> float:
    """helper function to check if str can be converted to float"""
    try:
        return float(num)
    except Exception as e:
        logger.warning(
            f"Error while trying to convert to float{e}",
            extra={"json_fields": LoggingExtras.PriceError},
        )
        return False


def format_price(price: str) -> str:
    price = re.sub(r",", ".", price)
    price = re.sub(r"\n|\t|\$|€", "", price)
    if price.endswith("."):
        price = price[:-1]
    return price
