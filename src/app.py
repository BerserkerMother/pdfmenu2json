import json
import logging

from flask import Flask, request
import dotenv

from logger import logger
from utils import extract_menu_items
from extractors import pdf, html, food_type_chain

# set up logging
log = logger.get_logger("pdf2menu")

pdf_chain = pdf.get_parsing_chain()
html_chain = html.get_parsing_chain()
category_chain = food_type_chain.get_food_type_chain()

app = Flask("menu2json")


@app.route("/pdf", methods=["POST"])
def pdf_convert():
    pdf_menu = request.files["menu"]
    chunks = pdf.get_chunks(pdf_menu=pdf_menu)
    menu_items = extract_menu_items(pdf_chain, category_chain, chunks)
    return menu_items


@app.route("/html", methods=["POST"])
def html_convert():
    menu_link = request.json["menu"]
    chunks = html.get_chunks(link=menu_link)
    menu_items = extract_menu_items(html_chain, category_chain, chunks)
    return menu_items


@app.route("/", methods=["GET"])
def greeting():
    return {"response": "Yes I do work"}


# app.run(host="localhost", port="1234")
