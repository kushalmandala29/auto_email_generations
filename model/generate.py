from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM
from dataclasses import dataclass
import json
import re

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
        "salutation": "your greeting",
        "body": "your email body",
        "closing": "your closing statement",
        "signature": "your signature"
    }
    Ensure the response is properly formatted JSON."""

    def parse_response(self,email_text: str) -> EmailContent:
    # Initialize dictionary to store the parts
        email_parts = {}
    
    # Split the text into sections using the '|' delimiter
        sections = re.findall(r'(?:\|(.*?)\||(\w+):)\s*(.*?)(?=(?:\|\w+\||[A-Za-z]+:)|\Z)', email_text, re.DOTALL)
    
    # Process each section
        for section_name, content in sections:
            section_name = section_name.strip().lower()
            content = content.strip()
        
            if section_name == "closing":
            # Split by "Best regards," or similar closing phrase
                parts = re.split(r'(?i)best regards,\s*', content)
                if len(parts) > 1:
                # Main closing text
                    email_parts["closing"] = parts[0].strip() + "\nBest regards,"
                # Get signature lines
                    signature_lines = [line.strip() for line in parts[1].strip().split('\n') if line.strip()]
                    email_parts["signature"] = "\n".join(signature_lines)
                else:
                    email_parts["closing"] = content
                    email_parts["signature"] = ""
            elif section_name in ["salutation", "body"]:
                email_parts[section_name] = content
    
    # Create EmailContent object
        return EmailContent(
            salutation=email_parts.get("salutation", ""),
            body=email_parts.get("body", ""),
            closing=email_parts.get("closing", ""),
            signature=email_parts.get("signature", "")
        )
    

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
        template = """Generate an email body content (NO subject line, NO 'From:', NO 'To:' fields) based on:

Context: {context}
Tone: {tone}
Purpose: {purpose}

{format_instructions}

Requirements:
1. Start directly with a greeting (e.g., "Dear [Name]," or "Hello,")
2. Write the main message body
3. Add a closing statement (e.g., "Best regards," or "Thank you,")
4. End with a signature
5. Use the specified tone throughout
6. Address the purpose clearly
7. Keep content relevant to context

DO NOT include:
- Subject line
- Email headers (From:, To:, Date:, etc.)
- Any metadata

The response must be ONLY the JSON object with these fields:
- salutation
- body
- closing
- signature"""

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
        
            # Create prompt
        prompt = self.create_prompt(context, tone, purpose)

            # Generate response
        response = self.llm.predict(prompt)

        # print(type(response))
        print(response)
        # return response
            # Parse and validate response
        email_content = self.parser.parse_response(response)

        # # content=prompt|self.llm|self.parser.parse_response
        # print(email_content)
            
        return {
            "parsed": email_content.dict(),
            "formatted": email_content.format()
        }
        # return {
        #     "parsed": content.dict(),
        #     "formatted": content.format()
        # }
        # except Exception as e:
        #     print(f"Debug - Raw response: {response}")  # For debugging
        #     raise RuntimeError(f"Email generation failed: {str(e)}")

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