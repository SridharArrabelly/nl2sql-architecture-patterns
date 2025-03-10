import os
#from dotenv import load_dotenv
#load_dotenv()
db_user = os.getenv("MySql_db_user")
db_password = os.getenv("MySql_db_password")
db_host = os.getenv("MySql_db_host")
db_name = os.getenv("MySql_db_name")

# LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
# LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

openai_api_base=os.getenv("AZURE_OPENAI_ENDPOINT")
openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION") 
azure_deployment="gpt-4-32k"
openai_api_key = os.getenv("AZURE_OPENAI_KEY") 
openai_api_type="azure"

from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
#from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.memory import ChatMessageHistory
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
#from langchain_openai import ChatOpenAI
from table_details import table_chain as select_table
from table_details import table_details as table_info
from prompts import final_prompt, answer_prompt
from prompts import answer_prompt

import streamlit as st

from langchain_openai import AzureChatOpenAI

@st.cache_resource
def get_chain():
    print("Creating chain")
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")    
    #llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    llm = AzureChatOpenAI(
        azure_endpoint=openai_api_base,
        openai_api_version=openai_api_version,
        azure_deployment=azure_deployment,
        openai_api_key=openai_api_key,
        openai_api_type=openai_api_type,
        temperature = 0 
    )
    generate_query = create_sql_query_chain(llm, db,final_prompt) 
    execute_query = QuerySQLDataBaseTool(db=db)
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    # chain = generate_query | execute_query
    chain = (
        RunnablePassthrough.assign(table_names_to_use=select_table) |
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | rephrase_answer
    )

    return chain

def create_history(messages):
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history


def invoke_chain(question,messages):
    chain = get_chain()
    history = create_history(messages)
    #response = chain.invoke({"question": question,"top_k":3,"messages":history.messages})
    response = chain.invoke({"input": question,"question": question,"table_details":table_info,"messages":history.messages})
    history.add_user_message(question)
    history.add_ai_message(response)
    return response