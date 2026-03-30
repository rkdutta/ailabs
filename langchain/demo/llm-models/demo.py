from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv

load_dotenv()

llm = OllamaLLM(model="glm-5:cloud", base_url="https://api.ollama.com")
response = llm.invoke("What is the capital of France?")
print(response)
