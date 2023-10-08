from langchain import PromptTemplate
from langchain.chains import SequentialChain, LLMChain
from langchain.llms import OpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser

llm = OpenAI(temperature=0.0)


def get_food_chain():
    # extracting food from menu
    fi_food = (
        "your response should be a list of comma separated values, eg: `foo, bar, baz`"
    )
    food_template = (
        "You are given a html text of a restaurant menu. The menu consists of foods with prices and ingridents."
        "Please extract only the foods in the menu.\nmenu:\n{document}.\n{fi_food}"
    )
    prompt_food = PromptTemplate(
        template=food_template,
        input_variables=["document"],
        partial_variables={"fi_food": fi_food},
        # output_parser=CommaSeparatedListOutputParser(),
    )
    food_chain = LLMChain(
        llm=llm,
        prompt=prompt_food,
        output_key="foods",
    )
    return food_chain


def get_price_chain():
    fi_price = "your response should be a list of food and their prices separated by ; , eg: `foo: 20$; bar: 10$; baz: 43$`"
    price_template = (
        "You are given a html text of a restaurant menu. The menu consists of foods with prices and ingridents."
        "Some foods may be grouped together and share the same price."
        "Extract the price for foods: {foods} from the html restaurant menu.\nmenu:\n{document}.\n{fi_price}."
    )
    prompt_price = PromptTemplate(
        template=price_template,
        input_variables=["foods", "document"],
        partial_variables={"fi_price": fi_price},
        # output_parser=CommaSeparatedListOutputParser(),
    )
    price_chain = LLMChain(
        llm=llm,
        prompt=prompt_price,
        output_key="menu",
    )
    return price_chain


def get_parsing_chain():
    food_chain = get_food_chain()
    price_chain = get_price_chain()

    language_chain = SequentialChain(
        chains=[food_chain, price_chain],
        input_variables=["document"],
        output_variables=["menu"],
    )
    return language_chain
