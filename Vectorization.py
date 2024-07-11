from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Load pdf file
loader = PyMuPDFLoader("The-art-of-hearing.pdf")
content = loader.load()

# Text splitter
splitter = RecursiveCharacterTextSplitter()
split_docs = splitter.split_documents(content)

# Create and Store Embeddings

#...Initialize embedding model
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2", 
                              model_kwargs={'device':'cpu'}, 
                              encode_kwargs = {"normalize_embeddings": False})

#...Initialize vector store
chromaDB = Chroma()

#...Store embeddings
store = chromaDB.from_documents(documents=split_docs, embedding=model, persist_directory="vectorDB")