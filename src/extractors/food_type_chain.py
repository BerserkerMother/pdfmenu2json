from langchain import PromptTemplate
from langchain.chains import SequentialChain, LLMChain
from langchain.llms import OpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser

llm = OpenAI(temperature=0.0)


def get_food_type_chain():
    fi_type = "your response should be a list of items and their categories separated by ; , eg: `foo: food; bar: drink; baz: food`"
    price_template = (
        "You are given a list of items. Your job is to decide whether the item category is drink or food"
        "\nitems:n{foods}.\n{fi_type}."
    )
    prompt_price = PromptTemplate(
        template=price_template,
        input_variables=["foods"],
        partial_variables={"fi_type": fi_type},
        # output_parser=CommaSeparatedListOutputParser(),
    )
    type_chain = LLMChain(
        llm=llm,
        prompt=prompt_price,
        output_key="foods",
    )
    return type_chain
