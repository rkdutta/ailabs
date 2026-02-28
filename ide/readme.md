### Setting Up Agentic IDE Locally

**Requirements**

1. **Integrated Development Environment (IDE)**: Visual Studio Code (VSCODE)
2. **Ollama**: A tool for pulling models locally using Ollama
3. **Connector Plugin**: continue.dev (facilitates integration of VSCODE with ollama)
4. **Install Models**:
    
    4.1. Chat models - to interact with the model using chat commands
    ```
    # all or any one of these models
    ollama pull llama3.1:8b
    ollama pull gpt-oss:20b
    ollama pull glm-4.7-flash
    ```

    4.2. Auto completion model - to complete the code using snippets

    ```
    ollama pull qwen2.5-coder:1.5b-base
    ```

    4.3. embedding - to index the source code and provide the ability the search / asking questions

    ```
    ollama pull nomic-embed-text:latest
    ```

