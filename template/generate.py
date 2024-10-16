from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM



class model:
    def __init__(self):
        self.template = """Question: {question}

Answer: Let's think step by step."""
        self.model = OllamaLLM(model="tinyllama")
        self.prompt = ChatPromptTemplate(self.template)

        self.chain = self.prompt | self.model
    def generate(self, inputs: str):
        return self.chain.invoke({"question": "What is LangChain?"})
# template = """Question: {question}

# Answer: Let's think step by step."""

# prompt = ChatPromptTemplate.from_template(template)
# model = OllamaLLM(model="tinyllama")

# chain = prompt | model

# chain.invoke({"question": "What is LangChain?"})