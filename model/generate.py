import os
# from langchain.llms import Ollama
from langchain.chains import LLMChain
# from test_generate import ModelConfig
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.callbacks.base import BaseCallbackHandler

# Optional: Set up the OpenAI API key if needed
# openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define a custom callback handler to monitor execution
class StructuringCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, **kwargs):
        """Executes at the start of the LLM process."""
        print("Starting data structuring process...")

    def on_llm_end(self, output, **kwargs):
        """Executes when the LLM process completes."""
        print("Data structuring complete.")

# Define the main class to handle data structuring
class DataStructurer:
    def __init__(self,model_name="mistral:7b", temperature=0.7):
        """Initializes the DataStructurer with an LLM and prompt template."""

        # self.config = ModelConfig()
        self.llm = OllamaLLM(
            model=model_name,
            temperature=temperature
        )
        
        
        self.prompt = self._create_prompt_template()
        self.callback_handler = StructuringCallbackHandler()
        self.structuring_chain = self._create_structuring_chain()

    

    def _create_prompt_template(self):
        """Defines the prompt template for structuring unstructured input data."""
        remail_prompt = PromptTemplate(
    template = """You are a professional email writer. Based on this request: {input_text}

Please write an email that includes:
1. A professional email body
2. An appropriate signature

Keep the tone professional and the content concise.

Format your response as:

[Email body]

[Signature]
""",
    input_variables=["input_text"]
)
        return remail_prompt

    def _create_structuring_chain(self):
        """Creates the LLMChain for structuring data using the defined LLM and prompt template."""
        return LLMChain(llm=self.llm, prompt=self.prompt, callbacks=[self.callback_handler])

    def structure_data(self, input_text):
        """
        Processes unstructured input data and transforms it into a structured format.
        
        Args:
            input_text (str): The raw input data to be structured.
            
        Returns:
            dict: The structured output data.
        """
        output = self.structuring_chain.invoke(input_text)
        return output['text']
        # try:
        #     output = self.structuring_chain.invoke(input_text)
        #     return output
        # except Exception as e:
        #     print(f"Error: {e}")
        #     return {
        #         "context": "Unknown",
        #         "tone": "professional but friendly",
        #         "purpose": "Unknown",
        #         # "enriched_data": []
        #     }
# Example usage:
# Example usage:
if __name__ == "__main__":
    data_structurer = DataStructurer()
    input_text = """
    Need to send update about the new product launch to stakeholders.
    """
    structured_output = data_structurer.structure_data(input_text)

    print(structured_output)
