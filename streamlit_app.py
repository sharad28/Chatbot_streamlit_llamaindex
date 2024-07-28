
from llama_index.llms.openai import OpenAI
from llama_index.core.readers.base import BaseReader
from llama_index.readers.microsoft_sharepoint import SharePointReader
from llama_index.core import VectorStoreIndex,ServiceContext,Document,SimpleDirectoryReader,StorageContext, load_index_from_storage
import openai
import os
import streamlit as st

from dotenv import load_dotenv
load_dotenv()
sharepoint_site_name="sharepointsite"

st.set_page_config(page_title="Chat with Custom data",layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = os.getenv('OPENAI_API_KEY')
st.title(f"Chat with SharePoint data")
st.info(f"Custom data received from SharePoint site name: {sharepoint_site_name}")

def save_index(index, directory="./saved_index"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    index.storage_context.persist(persist_dir=directory)

if "messages" not in st.session_state.keys():
    st.session_state.messages=[
        {"role": "assistant", "content": "Ask me a question from Knowledge base (custom data: SharePoint site)!"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    index_directory = "./saved_index"
    
    if os.path.exists(index_directory):
        with st.spinner(text='Loading saved index...'):
            storage_context = StorageContext.from_defaults(persist_dir=index_directory)
            index = load_index_from_storage(storage_context)
    else:
        with st.spinner(text='Loading and indexing data...'):
            loader = SharePointReader(
                client_id=os.getenv('client_id'),
                client_secret=os.getenv('client_secret'),
                tenant_id=os.getenv('tenant_id'),
            )

            try:
                docs = loader.load_data(
                    sharepoint_site_name="sharepointsite",
                    sharepoint_folder_path="internal_folder",
                    recursive=True
                )
            except Exception as e:
                print(e)
                return None

            index = VectorStoreIndex.from_documents(docs, show_progress=True)
            save_index(index)
    
    return index

index = load_data()

if 'chat_engine' not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True,
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

