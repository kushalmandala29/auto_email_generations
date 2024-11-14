import os
# from langchain.llms import Ollama
from langchain.chains import LLMChain
# from test_generate import ModelConfig

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
    def __init__(self,model_name="tinyllama", temperature=0.7):
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
        return PromptTemplate(
            template="""
            You are an AI assistant tasked with taking unstructured input data and transforming it into a structured format. The input data will be provided as a raw string. Your goal is to extract the relevant information and organize it into a coherent output.

            The output should be in the following format:
            ```json
            {{
              "context": "<context of the input data>",
              "tone": "<tone to be used, defaulting to 'professional but friendly' if not specified>",
              "purpose": "<purpose or intent of the input data>",
                }}

            If any required information (context, tone, or purpose) is missing from the input, please use the following default values:
            - Context: "Unknown"
            - Tone: "professional but friendly"
            - Purpose: "Unknown"

            Input: {input}

            Output:
            """,
            input_variables=["input"]
        )

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
        return output
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
