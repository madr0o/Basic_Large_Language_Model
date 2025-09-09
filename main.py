from sqlalchemy.orm import Session
from db import engine
from crud import upsert_collection
from validation import load_animal_catalog, is_valid_animal

from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException
from langchain_openai import ChatOpenAI
import re

response_schemas = [
    ResponseSchema(name="name", description="the name of an animal"),
    ResponseSchema(name="scientific_name", description="scientific name of an animal"),
    ResponseSchema(name="description", description="the description of the animals that user requested"),
    ResponseSchema(name="habitat", description="animal's natural habitat"),
    ResponseSchema(name="food", description="type of main animal food"),
    ResponseSchema(name="behaviour", description="characteristic animal behaviour"),
    ResponseSchema(name="unique", description="unique facts about the animals"),
    ResponseSchema(name="addition", description="useful information for animal visitors"),
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instruction = output_parser.get_format_instructions()

prompt = PromptTemplate(
    template = "you are a zoo keeper assitant. "
                "Only answer about real animals. "
                "If the input is not an animal, respond with 'Error: Input must be an animal.' "
                "explain about the animal: {animals}. "
                "use the following format:\n{format_instruction}",
    input_variables = ["animals"],
    partial_variables = {"format_instruction":format_instruction},
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = prompt | model | output_parser

animal_binomial_re = re.compile(r"^[A-Z][a-z]+ [a-z]+$")


catalog = load_animal_catalog(r"C:\Pribadi\Internship\Latihan_build_AI_app\Zoo Keeper Assistant\animals_catalog.csv")

def save_to_mysql(user_input: str):
    resolved = is_valid_animal(user_input, catalog, treshold=70)
    if not resolved:
        print("Error: Input bukan hewan.")
        return
    
    result = chain.invoke({"animals": resolved["name"]})

    if not result.get("scientific_name"):
        result["scientific_name"] = resolved["scientific_name"]
    if not result.get("name"):
        result["name"] = resolved["name"]

    print(result)

    with Session(engine) as session:
        obj = upsert_collection(session, result)
        print(f"\nTersimpan id={obj.id}, sci={obj.scientific_name}")

if __name__ == "__main__":
    user_input = input("What animals are you interested in? ")
    save_to_mysql(user_input)