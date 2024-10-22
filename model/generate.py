from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM



# class model_ollama:
#     def __init__(self):
#         self.template = """Question: {question}

# Answer: Let's think step by step."""
#         self.model = OllamaLLM(model="tinyllama")
#         self.prompt = ChatPromptTemplate(self.template)

#         self.chain = self.prompt | self.model
#     def generatess(self, inputs: str):
#         self.inputs = inputs
#         return self.chain.invoke({"question": self.inputs})
    


# mod = model_ollama()
# mod.generatess("What is LangChain?")


def generate(input:str):
    template = """Question: {question}
    Answer: Let's think step by step."""
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="tinyllama")
    chain = prompt | model
    return chain.invoke({"question": input})



# print(generate("What is LangChain?"))
