import streamlit as st
#from openai import OpenAI
from langchain_utils import invoke_chain
import os
#from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

# Load config values
db_user = os.getenv("MySql_db_user")
db_password = os.getenv("MySql_db_password")
db_host = os.getenv("MySql_db_host")
db_name = os.getenv("MySql_db_name")
db_port = os.getenv("MySql_db_port")

LANGCHAIN_TRACING_V2 = "false"
LANGCHAIN_API_KEY = os.environ["LANGCHAIN_API_KEY"]

openai_api_base = os.getenv("AZURE_OPENAI_ENDPOINT") 
openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION") 
azure_deployment = "gpt-4-32k"
openai_api_key = os.getenv("AZURE_OPENAI_KEY") 
openai_api_type = "azure"

search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_AI_SEARCH_KEY")
index = "sqlsearchindex"

# Create an instance of chat llm
client = AzureChatOpenAI(
    azure_endpoint=openai_api_base,
    openai_api_version=openai_api_version,
    azure_deployment=azure_deployment,
    openai_api_key=openai_api_key,
    openai_api_type=openai_api_type,
    temperature = 0
)

st.title("Natural Language to SQL Chatbot")
st.subheader("Tools: MySql, AzureOpenAI, Langchain, Python, Streamlit")

# Set OpenAI API key from Streamlit secrets
#client = OpenAI(api_key=OPENAI_API_KEY)

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-32k"

# Initialize chat history
if "messages" not in st.session_state:
    # print("Creating session state")
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            response = invoke_chain(prompt,st.session_state.messages)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})