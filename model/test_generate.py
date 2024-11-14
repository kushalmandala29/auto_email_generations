import os
from langchain_ollama.llms import OllamaLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler

class EmailGeneratorCallback(BaseCallbackHandler):
    def on_llm_start(self, serialized, **kwargs):
        print("Starting email generation...")

    def on_llm_end(self, output, **kwargs):
        print("Email generation complete.")

class EmailGenerator:
    def __init__(self, model_name="tinyllama", temperature=0.7):
        """Initialize the EmailGenerator with specified model and temperature."""
        self.llm = OllamaLLM(
            model=model_name,
            temperature=temperature
        )
        
        self.prompt = self._create_prompt_template()
        self.callback_handler = EmailGeneratorCallback()
        self.email_chain = self._create_email_chain()

    def _create_prompt_template(self):
        """Create a prompt template for email generation."""
        return PromptTemplate(
            template="""
            Generate an email content using the following structured information:

            Context: {context}
            Tone: {tone}
            Purpose: {purpose}

            Additional Data Points to incorporate:
            {enriched_data}

            Instructions for email generation:
            1. Create a subject line that clearly reflects the context and purpose
            2. Use the specified tone: {tone}
            3. Address the stated purpose: {purpose}
            4. Incorporate the provided data points naturally into the narrative
            5. Ensure the email flows logically and maintains professional formatting
            6. Use bullet points or sections if needed to present data clearly
            7. Make sure all key information from the enriched data is utilized

            Required Output Format:

            Subject: [Generate a clear, relevant subject line]

            [Write the email body that:
            - Opens with an appropriate greeting
            - Presents information in a structured way
            - Incorporates all relevant data points
            - Maintains the specified tone
            - Achieves the stated purpose]

            [Add an appropriate closing]
            """,
            input_variables=["context", "tone", "purpose", "enriched_data"]
        )

    def _create_email_chain(self):
        """Create the LLMChain for email generation."""
        return LLMChain(
            llm=self.llm, 
            prompt=self.prompt, 
            callbacks=[self.callback_handler]
        )

    def generate_email(self, context, tone="professional", purpose="inform"):
        """
        Generate an email based on the provided parameters.
        
        Args:
            context (str): The context or background information for the email
            tone (str): The desired tone (e.g., professional, friendly, formal)
            purpose (str): The purpose or goal of the email
            
        Returns:
            str: The generated email content
        """
        try:
            output = self.email_chain.invoke({
                "context": context,
                "tone": tone,
                "purpose": purpose
            })
            return output["text"]
        except Exception as e:
            print(f"Error generating email: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Initialize the email generator
    email_gen = EmailGenerator()
    
    # Example parameters
    context = "New product launch of our AI-powered analytics platform scheduled for next month"
    tone = "professional but enthusiastic"
    purpose = "inform stakeholders about the upcoming launch and key features"
    
    # Generate the email
    email = email_gen.generate_email(
        context=context,
        tone=tone,
        purpose=purpose
    )
    
    if email:
        print("Generated Email:")
        print("-" * 50)
        print(email)

