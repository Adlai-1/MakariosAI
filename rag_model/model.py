import configparser
from pinecone import Pinecone
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain, create_history_aware_retriever

config = configparser.ConfigParser()
config.read("config.ini")

# initialize
llm_model = ChatGroq(model=config['SERVER']['model'], api_key=config['SERVER']['key'])
embedding_model = HuggingFaceEmbeddings(model_name=config['SERVER']['embedding'])

try:
    pc = Pinecone(api_key=config['SERVER']['vector'])
    idx = pc.Index(config['SERVER']['index'])
except:
    print("Unable to initialize VectorDB!")

vector =  PineconeVectorStore(idx, embedding_model).as_retriever()

# prompts
context = """
Given a chat history and the latest user question \
which might reference context in the chat history, \
formulate a standalone question which can be understood \
without the chat history. Do NOT answer the question, \
just reformulate it if needed, otherwise return it as it is.
"""
context_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", context),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)

llm = """
You name is MakariosAI and you help people \
have a deep understanding of all the books \
authored by Bishop Dag Heward-Mills. \
Except for introductory messages, like Hello etc, \
always use the retrieved context below to answer questions. \
If you don't know the answer, let it be known. \
Lastly, be very conversational when giving responses.\n\n
{context}
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", llm),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)

# rag chain setup
history_chain = create_history_aware_retriever(llm_model, vector, context_prompt)
qa_chain = create_stuff_documents_chain(llm_model, prompt)
main_chain = create_retrieval_chain(history_chain, qa_chain)


def store_chat(memory: list, query: str, resp: str):
    memory.extend([HumanMessage(content=query), AIMessage(content=resp)])

def call_rag(input: str, chat_memory: dict) -> str:
    resp = main_chain.invoke({"input": input, "history": chat_memory})
    #store_chat(chat_memory, input, resp["answer"])
    return resp["answer"]