import os
import re
from typing import Dict, List

from logger import logger as log

logger = log.get_logger("utils")


def llm_to_json(menu_dict: Dict, items_unstructured) -> Dict:
    """Adds llm menu item findings to a dictionary for api"""
    logger.info(items_unstructured)
    for item in items_unstructured.split(";"):
        food_price = item.split(":")
        logger.info(food_price)
        if len(food_price) == 2:
            name = re.sub(r"\n|\t", "", food_price[0])
            price = format_price(food_price[1])
            price = to_float(price)
            if not price:
                logger.warnning(f"[ ITEM ] [ PRICE ]{item}")
        else:
            logger.warnning(f"[ ITEM ] {item}")
            menu_dict["menu"].append({"name": name.lower().strip(), "price": price})
    return menu_dict


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
