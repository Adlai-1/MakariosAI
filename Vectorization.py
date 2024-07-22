from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from pinecone import  Pinecone
from langchain_pinecone import PineconeVectorStore

# Load pdf file
loader = PyMuPDFLoader("Those-who-are-proud.pdf")
content = loader.load()

# Text splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
split_docs = splitter.split_documents(content)

# Create and Store Embeddings

#...Initialize embedding model
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2", 
                              model_kwargs={'device':'cpu'}, 
                              encode_kwargs = {"normalize_embeddings": False})


pc = Pinecone(api_key='4e7a267a-de2a-4b88-aae8-76fe72fe59a0')

idx = pc.Index("books")

store =  PineconeVectorStore(idx, model)

print(store.similarity_search("Voice of God", k=5))