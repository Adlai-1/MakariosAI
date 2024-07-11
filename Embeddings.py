from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

#...Initialize embedding model
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2", 
                              model_kwargs={'device':'cpu'}, 
                              encode_kwargs ={"normalize_embeddings": False})

# Retrieve vector embeddings from persistant memory
embeddings = Chroma(persist_directory="vectorDB", embedding_function=model)

# Build Retriever from Vector Store
retriever = embeddings.as_retriever(search_kwargs={"k": 8})