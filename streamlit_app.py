
from llama_index.llms.openai import OpenAI

from llama_index.core.readers.base import BaseReader
from llama_index.readers.microsoft_sharepoint import SharePointReader
from llama_index.core import VectorStoreIndex,ServiceContext,Document,SimpleDirectoryReader
import openai
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Chat with personal data",layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = os.getenv('OPENAI_API_KEY')
st.title("Chat with latest Data")
st.info("Check out rag")

if "messages" not in st.session_state.keys():
    st.session_state.messages=[
        {"role": "assistant", "content": "Ask me a question about Streamlit's open-source Python library!"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text='loading and indexing data'):
        print("enter the loader")
        print({
    "client_id":os.getenv('client_id'),
    "client_secret":os.getenv('client_secret'),
    "tenant_id":os.getenv('tenant_id')})
        loader = SharePointReader(
    client_id=os.getenv('client_id'),
    client_secret=os.getenv('client_secret'),
    tenant_id=os.getenv('tenant_id'),
        sharepoint_site_name="sharepointsite",
        sharepoint_folder_path="internal_folder")
        print(f"loader : {loader}")
        try:
            docs = loader.load_data(
        sharepoint_site_name="sharepointsite",
        sharepoint_folder_path="internal_folder",
        recursive=True)
        except Exception as e:
            print(e)
        # reader = SimpleDirectoryReader('data')
        # docs = reader.load_data()  
        print(docs)      
        index = VectorStoreIndex.from_documents(docs,show_progress=True)
        return index
    
index = load_data()

if 'chat_engine' not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True
    )

if prompt :=st.chat_input("Your question"):
    st.session_state.messages.append({'role':'user','content':prompt})

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

if st.session_state.messages[-1]['role'] != 'assistant':
    with st.chat_message('assistant'):
        with st.spinner('thinking.....'):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {'role':'assistant','content':response.response}
            st.session_state.messages.append(message)

