import configparser
from Embeddings import retriever
from langchain_groq import ChatGroq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

config = configparser.ConfigParser()
config.read("config.ini")

# Save Chat history
def saveChat(query: str, response: dict, storage: list):
    storage.extend(
        [
            HumanMessage(content=query),
            AIMessage(response['answer'])
        ]
    )

# Generation Section

# Initialize model
model = ChatGroq(model=str(config['SERVER']['model']), api_key=str(config['SERVER']['key']))

# Setup for History retriever
ChatHistoryPrompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

ContextPrompt = ChatPromptTemplate.from_messages(
    [
        ("system", ChatHistoryPrompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Setup for chat history and context
system_prompt = (
    "Use the retrieved context below to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Also be very conversational when giving responses."
    "\n\n"
    "{context}"
)

user_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# RAG Chains
Processchain = create_stuff_documents_chain(model, user_prompt)
Contextchain = create_history_aware_retriever(model, retriever, ContextPrompt)
RAGchain = create_retrieval_chain(Contextchain, Processchain)