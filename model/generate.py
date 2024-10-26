from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from dataclasses import dataclass
import json

@dataclass
class ModelConfig:
    """Configuration for the LLM model"""
    model_name: str = "tinyllama"
    temperature: float = 0.7

class EmailContent(BaseModel):
    """Schema for email content"""
    subject: str = Field(..., description="The email subject line")
    salutation: str = Field(..., description="The opening greeting")
    body: str = Field(..., description="The main content")
    closing: str = Field(..., description="The closing statement")
    signature: str = Field(..., description="The signature line")

    def format(self) -> str:
        """Format the email content into a string"""
        return f"""Subject: {self.subject}

{self.salutation}

{self.body}

{self.closing}

{self.signature}"""

class EmailParser:
    """Handles parsing and validation of email content"""
    def __init__(self):
        self.response_schemas = [
            ResponseSchema(name="subject", description="The email subject line"),
            ResponseSchema(name="salutation", description="The opening greeting of the email"),
            ResponseSchema(name="body", description="The main content of the email"),
            ResponseSchema(name="closing", description="The closing statement of the email"),
            ResponseSchema(name="signature", description="The signature line of the email")
        ]
        self.parser = StructuredOutputParser.from_response_schemas(self.response_schemas)

    def get_format_instructions(self) -> str:
        """Get format instructions for the parser"""
        return """Please provide the email content in the following JSON format:
{
    "subject": "your subject line",
    "salutation": "your greeting",
    "body": "your email body",
    "closing": "your closing statement",
    "signature": "your signature"
}
Ensure the response is properly formatted JSON."""

    def parse_response(self, response: str) -> EmailContent:
        """Parse LLM response into EmailContent with better error handling"""
        try:
            # Try to extract JSON if it's wrapped in other text
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                parsed = json.loads(json_str)
            else:
                raise ValueError("No JSON object found in response")

            # Validate required fields
            required_fields = {"subject", "salutation", "body", "closing", "signature"}
            missing_fields = required_fields - set(parsed.keys())
            
            if missing_fields:
                raise ValueError(f"Missing required fields: {missing_fields}")

            return EmailContent(**parsed)
        except Exception as e:
            raise ValueError(f"Failed to parse response: {str(e)}\nResponse: {response}")

class EmailGenerator:
    """Main email generation class"""
    def __init__(self, config: Optional[ModelConfig] = None):
        """Initialize EmailGenerator with configuration"""
        self.config = config or ModelConfig()
        self.llm = OllamaLLM(
            model=self.config.model_name,
            temperature=self.config.temperature
        )
        self.parser = EmailParser()

    def create_prompt(self, context: str, tone: str, purpose: str) -> str:
        """Create a formatted prompt with explicit JSON instructions"""
        template = """Please generate a professional email based on the following information:

Context: {context}
Tone: {tone}
Purpose: {purpose}

{format_instructions}

Remember to:
1. Use the specified tone throughout the email
2. Address the purpose clearly in the body
3. Keep the content relevant to the context
4. Format the output as valid JSON

The response should ONLY contain the JSON object, no additional text."""

        return PromptTemplate(
            template=template,
            input_variables=["context", "tone", "purpose"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        ).format(
            context=context,
            tone=tone,
            purpose=purpose
        )

    def generate(self, 
                context: str, 
                tone: str, 
                purpose: str) -> Dict[str, str]:
        """Generate an email based on the provided parameters"""
        try:
            # Create prompt
            prompt = self.create_prompt(context, tone, purpose)

            # Generate response
            response = self.llm.predict(prompt)
            
            # Parse and validate response
            email_content = self.parser.parse_response(response)
            
            return {
                "parsed": email_content.dict(),
                "formatted": email_content.format()
            }
        except Exception as e:
            print(f"Debug - Raw response: {response}")  # For debugging
            raise RuntimeError(f"Email generation failed: {str(e)}")

def main():
    """Example usage of EmailGenerator"""
    # Initialize generator
    config = ModelConfig(temperature=0.7)
    generator = EmailGenerator(config)

    # Example parameters
    params = {
        "context": "Client meeting about website redesign project",
        "tone": "professional but friendly",
        "purpose": "summarize key points and outline next steps"
    }

    try:
        # Generate email
        result = generator.generate(**params)
        print("Generated Email:")
        print(result["formatted"])
    except Exception as e:
        print(f"Error generating email: {str(e)}")

if __name__ == "__main__":
    main()