examples = [
    {
        "input": "List all customers in France with a credit limit over 20,000.",
        "query": "SELECT * FROM customers WHERE country = 'France' AND creditLimit > 20000;"
    },
    {
        "input": "Get the highest payment amount made by any customer.",
        "query": "SELECT MAX(amount) FROM payments;"
    },
    {
        "input": "Show product details for products in the 'Motorcycles' product line.",
        "query": "SELECT * FROM products WHERE productLine = 'Motorcycles';"
    },
    {
        "input": "Retrieve the names of employees who report to employee number 1002.",
        "query": "SELECT firstName, lastName FROM employees WHERE reportsTo = 1002;"
    },
    {
        "input": "List all products with a stock quantity less than 7000.",
        "query": "SELECT productName, quantityInStock FROM products WHERE quantityInStock < 7000;"
    },
    {
     'input':"what is price of `1968 Ford Mustang`",
     "query": "SELECT `buyPrice`, `MSRP` FROM products  WHERE `productName` = '1968 Ford Mustang' LIMIT 1;"   
    }
]

from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
#from langchain_openai import OpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings
import streamlit as st
import os

# Load config values
db_user = os.getenv("MySql_db_user")
db_password = os.getenv("MySql_db_password")
db_host = os.getenv("MySql_db_host")
db_name = os.getenv("MySql_db_name")
db_port = os.getenv("MySql_db_port")

openai_api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION") 
azure_deployment = "gpt-4-32k"
openai_api_key = os.getenv("AZURE_OPENAI_KEY") 
openai_api_type = "azure"

search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_AI_SEARCH_KEY")
index = "sqlsearchindex"

embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-ada-002",
    openai_api_version=openai_api_version,
    azure_endpoint=openai_api_base,
    api_key=openai_api_key,
)

@st.cache_resource
def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        Chroma,
        k=2,
        input_keys=["input"],
    )
    return example_selector