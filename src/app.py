import json
import logging

from flask import Flask, request
import dotenv

from logger import logger
from utils import llm_to_json, get_parsing_chain, get_chunks

# set up logging
log = logger.get_logger("pdf2menu")

the_chain = get_parsing_chain()

app = Flask("menu2json")


@app.route("/convert", methods=["GET", "POST"])
def convert():
    pdf_menu = request.files["menu"]
    log.debug("err  ")
    chunks = get_chunks(pdf_menu=pdf_menu)
    menu_items = {"menu": []}
    for chunk in chunks:
        log.info(chunk)
        items_unstructured = the_chain.run(chunk)
        llm_to_json(menu_dict=menu_items, items_unstructured=items_unstructured)
    return menu_items


@app.route("/", methods=["GET"])
def greeting():
    return {"response": "Yes I do work"}


# app.run(host="localhost", port="1234")
