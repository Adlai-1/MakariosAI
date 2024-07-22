from langserve import RemoteRunnable

chat_history = []

sample = RemoteRunnable("http://localhost:8000/ask/")

sample.ainvoke({'input': 'Cars', 'chat_history': chat_history})