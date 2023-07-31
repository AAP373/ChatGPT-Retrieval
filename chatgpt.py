import os
import sys
from openpyxl import load_workbook
import pandas as pd
from docx import Document
from funcoms import get_loader_cls, WordLoader, JSONMod
import openai
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, PDFMinerLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
import constants

data_directory = constants.DATA_DIRECTORY
os.environ["OPENAI_API_KEY"] = constants.APIKEY
PERSIST = constants.PERSIST


def generate_response(query):
    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        index = VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        index_creator = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"} if PERSIST else {})
        loaders = []
        for filename in os.listdir(data_directory):
            file_extension = os.path.splitext(filename)[-1]
            loader_cls = get_loader_cls(file_extension)
            if loader_cls is not None:
                loader = loader_cls(os.path.join(data_directory, filename))
                loaders.append(loader)
        if loaders:
            index = index_creator.from_loaders(loaders)
        else:
            print("No valid files found in the data directory.")

    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-3.5-turbo"),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
    )
    return chain.run(query)

if __name__ == "__main__":
    query = sys.argv[1]
    print(generate_response(query))

