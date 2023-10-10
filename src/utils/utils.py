import os
import re
from typing import Dict, List

import google.cloud.logging

from logger import logger as log
from logger import LoggingExtras


logger = log.get_logger("utils")

client = google.cloud.logging.Client()
client.setup_logging()


def llm_to_json(menu_dict: Dict, items_unstructured) -> Dict:
    """Adds llm menu item findings to a dictionary for api"""
    foods_name = []  # for categorizing
    logger.info(items_unstructured)
    for item_price in items_unstructured.split(";"):
        food_price = item_price.split(":")
        logger.info(food_price, extra={"json_fields": LoggingExtras.Success})
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
