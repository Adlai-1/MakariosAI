from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

#...Initialize embedding model
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2", 
                              model_kwargs={'device':'cpu'}, 
                              encode_kwargs ={"normalize_embeddings": False})

