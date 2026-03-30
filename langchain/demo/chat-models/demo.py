from langchain_ollama.chat_models import ChatOllama
from dotenv import load_dotenv

load_dotenv()

# get model
llm = ChatOllama(model="glm-5:cloud", base_url="https://api.ollama.com")

# invoke
response = llm.invoke("What is the capital of France?")
print(response)
