from langchain_ollama.llms import OllamaLLM
from dotenv import load_dotenv

load_dotenv()

# get model
llm = OllamaLLM(model="glm-5:cloud", base_url="https://api.ollama.com")

# invoke
response = llm.invoke("What is the capital of France?")
print(response)

# important: unlike llmmodels, chatmodels return a list of messages, so we need to extract the content from the first message
