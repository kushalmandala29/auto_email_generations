import os
import re
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

    # def extract_latest(key, text):
    #     """Extract the latest occurrence of a key-value pair"""
    #     pattern = f"{key}.*?[\"']([^\"']+)[\"']"
    #     matches = re.findall(pattern, text, re.IGNORECASE)
    #     return matches[-1] if matches else None
    
    def get_latest_values(self,input_str):
        def extract_latest(key, text):
            """Extract the latest occurrence of a key-value pair"""
            pattern = f"{key}.*?[\"']([^\"']+)[\"']"
            matches = re.findall(pattern, text, re.IGNORECASE)
            return matches[-1] if matches else None
    
        """Helper function to extract the latest values from input"""
        return {
        "context": context if (context := extract_latest("context", input_str)) else "Unknown",
        "tone": tone if (tone := extract_latest("tone", input_str)) else "professional but friendly",
        "purpose": purpose if (purpose := extract_latest("purpose", input_str)) else "Unknown"
    }

    

    def _create_prompt_template(self):
        """Defines the prompt template for structuring unstructured input data."""
        return PromptTemplate(
    input_variables=["input"],
    template="""
    Given the input text:
    {input}

    Provide a detailed analysis of the input in the form of a dictionary with the following keys:

    Context:
    - Describe the overall context or situation surrounding the input text. What is the background or setting?
    - Identify any key entities, stakeholders, or important details that provide context.
    - Summarize the main topic or subject matter of the input.

    Tone:
    - Describe the overall tone or emotional quality of the input text.
    - Is the tone formal or informal? Friendly or professional? Persuasive or informative?
    - Identify any specific language, word choices, or stylistic elements that contribute to the tone.

    Purpose:
    - Determine the main purpose or intent behind the input text.
    - Is the purpose to inform, persuade, request, express an opinion, or something else?
    - What specific goal or outcome does the input text seem to be working towards?

    Please provide your analysis in the form of a dictionary with the above key-value pairs.
    """
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
        
        try:
            output_unstruture = self.structuring_chain.invoke(input_text)

            # output= self.get_latest_values(output_unstruture)
            return output_unstruture
        except Exception as e:
            print(f"Error: {e}")
            return {
                "context": "Unknown",
                "tone": "professional but friendly",
                "purpose": "Unknown",
                # "enriched_data": []
            }
# Example usage:
# Example usage:
if __name__ == "__main__":
    data_structurer = DataStructurer()
    input_text = """
    Need to send update about the new product launch to stakeholders.
    """
    structured_output = data_structurer.structure_data(input_text)

    print(structured_output)
