import os
import pandas as pd
import streamlit as st
from operator import itemgetter
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


#llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
from typing import List

openai_api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION") 
azure_deployment = "gpt-4-32k"
openai_api_key = os.getenv("AZURE_OPENAI_KEY") 
openai_api_type = "azure"

search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_AI_SEARCH_KEY")
index = "sqlsearchindex"

#os.environ["OPENAI_API_KEY"] = ""

# Create an instance of chat llm
llm = AzureChatOpenAI(
    azure_endpoint=openai_api_base,
    openai_api_version=openai_api_version,
    azure_deployment=azure_deployment,
    openai_api_key=openai_api_key,
    openai_api_type=openai_api_type,
    temperature = 0
)

@st.cache_data
def get_table_details():
    # Read the CSV file into a DataFrame
    table_description = pd.read_csv("database_table_descriptions.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + row['Table'] + "\n" + "Table Description:" + row['Description'] + "\n\n"
    return table_details

class Table(BaseModel):
    """Table in SQL database."""
    name: str = Field(description="Name of table in SQL database.")

class Tables(BaseModel):
    """Tables in SQL database."""
    # Creates a model so that we can extract multiple entities.
    name: List[Table]

def get_tables(tables: List[Table]) -> List[str]:
    tables  = [table.name for table in tables]
    return tables


# table_names = "\n".join(db.get_usable_table_names())
table_details = get_table_details()

table_details_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Return the names of ALL the table names that MIGHT be relevant to the user question. Remember to include ALL POTENTIALLY RELEVANT table names, even if you're not sure that they're needed.The tables are:  {table_details}",
        ),

        ("human", "{input}"),
    ]
)

def extract_table_names(tables: Tables) -> List[str]:
    return [table.name for table in tables.name]

table_chain = table_details_prompt | llm.with_structured_output(schema=Tables) | extract_table_names

