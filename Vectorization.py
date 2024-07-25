"""
This module is independent of any sub-module in this project.
This file contains the codes used to embedded texts from the books and
upload vector embeddings into a remote vector store (i.e. Pinecone) 
"""
import configparser
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from pinecone import  Pinecone

# open config file...
config = configparser.ConfigParser()
config.read("config.ini")

"""# Load pdf file
loader = PyMuPDFLoader("Those-who-are-proud.pdf")
content = loader.load()

# Text splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
split_docs = splitter.split_documents(content)"""

# Create and Store Embeddings

#...Initialize embedding model
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2", 
                              model_kwargs={'device':'cpu'}, 
                              encode_kwargs = {"normalize_embeddings": False})

#...Initialize vector store
pc = Pinecone(config['SERVER']['vector'])
idx = pc.Index("books")

#...Upload vector embeddings