import json
from typing import List
from dotenv import load_dotenv

from langchain import PromptTemplate
from langchain.chains import SequentialChain, LLMChain
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.output_parsers import CommaSeparatedListOutputParser

from flask import Flask, request

load_dotenv()

# text splitter for chatGPT 3.5
text_splitter = TokenTextSplitter(
    chunk_size=768, chunk_overlap=32, model_name="gpt-3.5-turbo"
)


def get_splitted_text(text: str) -> List[str]:
    return text_splitter.split_text(text)


def get_parsing_chain():
    llm = OpenAI(temperature=0.0, top_p=1)

    # extracting food from menu
    fi_food = (
        "your response should be a list of comma separated values, eg: `foo, bar, baz`"
    )
    food_template = (
        "You are given a menu of a restaurant. The menu consists of foods and their ingridents."
        "Be precise List all foods this restaurant menu offers. Do not list food ingridents.\n{document}.\n{fi_food}"
    )
    prompt_food = PromptTemplate(
        template=food_template,
        input_variables=["document"],
        partial_variables={"fi_food": fi_food},
        output_parser=CommaSeparatedListOutputParser(),
    )
    food_chain = LLMChain(llm=llm, prompt=prompt_food, output_key="foods")

    fi_price = "your response should be a list of food and their prices, eg: `foo: 20$, bar: 10$, baz: 43$`"
    price_template = (
        "Your task is to find prices for each food in a restaurant menu. Some foods may be grouoped together"
        "and share the same price."
        "Be precise and extract the price for foods: {foods} from the restaurant menu\n{document}.\n{fi_price}."
    )
    prompt_price = PromptTemplate(
        template=price_template,
        input_variables=["foods", "document"],
        partial_variables={"fi_price": fi_price},
        # output_parser=CommaSeparatedListOutputParser(),
    )
    price_chain = LLMChain(llm=llm, prompt=prompt_price, output_key="menu")

    language_chain = SequentialChain(
        chains=[food_chain, price_chain],
        input_variables=["document"],
        output_variables=["menu"],
        verbose=True,
    )

    return language_chain


the_chain = get_parsing_chain()

app = Flask("menu2json")


@app.route("/convert", methods=["GET"])
def convert():
    pdf_path = request.json["path"]
    doc = UnstructuredPDFLoader(pdf_path).load()[0].page_content
    chunks = get_splitted_text(doc)
    print(len(chunks))

    menu_items = dict()
    for chunk in chunks:
        items_unstructured = the_chain.run(chunk)
        for item in items_unstructured.split(","):
            food_price = item.split(":")
            if len(food_price) == 2:
                menu_items[food_price[0]] = food_price[1]

    return menu_items


app.run(host="localhost", port=1234)
