import json
import logging

from flask import Flask, request
import dotenv

from logger import logger
from utils import llm_to_json
from extractors import pdf, html

# set up logging
log = logger.get_logger("pdf2menu")

pdf_chain = pdf.get_parsing_chain()
html_chain = html.get_parsing_chain()

app = Flask("menu2json")

@app.route("/pdf", methods=["POST"])
def pdf_convert():
    pdf_menu = request.files["menu"]
    chunks = pdf.get_chunks(pdf_menu=pdf_menu)
    menu_items = {"menu": []}
    for chunk in chunks:
        # log.info(chunk)
        items_unstructured = pdf_chain.run(chunk)
        llm_to_json(menu_dict=menu_items, items_unstructured=items_unstructured)
    return menu_items


@app.route("/html", methods=["POST"])
def html_convert():
    menu_link = request.json["menu"]
    chunks = html.get_chunks(link=menu_link)
    menu_items = {"menu": []}
    for chunk in chunks:
        # log.info(chunk)
        items_unstructured = html_chain.run(chunk)
        llm_to_json(menu_dict=menu_items, items_unstructured=items_unstructured)
    return menu_items


@app.route("/", methods=["GET"])
def greeting():
    return {"response": "Yes I do work"}


# app.run(host="localhost", port="1234")
