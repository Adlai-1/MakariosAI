from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langserve import RemoteRunnable

# Initialize the RemoteRunnable with the server URL
joke_chain = RemoteRunnable("http://localhost:8000/ask/")

# Provide input as a list of dictionaries
input_data = {"input": [{"type": "human", "content": "Hello"}]} # Ensuring the input is a sequence of dictionaries

# Invoke the remote runnable with the modified input
response = joke_chain.invoke(input_data, config={"configurable": {"session_id": "baz"}})

print(response)
