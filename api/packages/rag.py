# RAG Model
#imports
import configparser
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.runnables import RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

config = configparser.ConfigParser()
config.read("config.ini")

#...Initialize embedding model
model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2", 
                              model_kwargs={'device':'cpu'}, 
                              encode_kwargs ={"normalize_embeddings": False})

# Initialize vector store
try:
    pc = Pinecone(api_key=config['SERVER']['vectorStore'])
    idx = pc.Index(config['SERVER']['index'])
except:
    print("Unable to initialize VectorDB!")

#...Initialize vector store
store =  PineconeVectorStore(idx, model)

#...Initialize LLm
groq = ChatGroq(model=str(config['SERVER']['model']), api_key=str(config['SERVER']['key']))

# LLM prompt
system_prompt = (
    "You name is MakariosAI and you help people "
    "have a deep understanding of all the books in "
    "the Makarios authored by Bishop Dag Heward-Mills. "
    "Except for introductory messages, always "
    "use the retrieved context below to answer "
    "the question. If you don't know the answer, let it be known "
    "Lastly, be very conversational when giving responses."
    "\n\n"
    "{context}"
)

user_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

def extract_query(input_data):
    if isinstance(input_data, list) and len(input_data) > 0:
        return input_data[0].get('content', '')
    return input_data if isinstance(input_data, str) else ''

input = RunnableParallel(
    {
        "context": RunnableLambda(extract_query) | store.as_retriever(search_kwargs={"k": 5}),
        "input": RunnablePassthrough()
    }
)

rag = input | user_prompt | groq | StrOutputParser()

chat_histories = {}

def get_chat_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in chat_histories:
        chat_histories[session_id] = ChatMessageHistory()
    return chat_histories[session_id]

chain = RunnableWithMessageHistory(
    rag,
    get_chat_history,
    input_messages_key="input"
)