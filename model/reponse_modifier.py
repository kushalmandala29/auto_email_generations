from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, List
import re
from datetime import datetime



class ProcessedInput(BaseModel):
    """Pydantic model for structured output"""
    context: str = Field(description="The main context or subject matter")
    tone: str = Field(description="The tone for communication")
    purpose: str = Field(description="The goal or objective")
    key_points: List[str] = Field(description="Extracted key points from the context")
    related_topics: List[str] = Field(description="Related topics for context enrichment")
    suggested_actions: List[str] = Field(description="Recommended next steps")

class DataProcessor:
    def __init__(self, model_name="mistral"):
        """Initialize the processor with specified Ollama model"""
        self.llm = Ollama(model=model_name)
        self.output_parser = PydanticOutputParser(pydantic_object=ProcessedInput)
        self.default_tone = "professional but friendly"
        
        # Initialize prompt templates
        self.structure_prompt = PromptTemplate(
            template="""
            Analyze the following input and structure it into a formal format.
            Extract or infer the context, tone (if not specified, use professional but friendly), and purpose.
            Also identify key points, related topics, and suggest actions.

            Input: {raw_input}

            {format_instructions}

            Provide a comprehensive analysis and structure the output accordingly.
            """,
            input_variables=["raw_input"],
            partial_variables={"format_instructions": self.output_parser.get_format_instructions()}
        )

        self.enrichment_prompt = PromptTemplate(
            template="""
            Based on the following structured information, provide additional context and insights:
            {structured_data}

            Please analyze this information and provide:
            1. Additional relevant context
            2. Potential implications
            3. Related considerations
            4. Best practices

            Keep the tone {tone} while providing these insights.
            """,
            input_variables=["structured_data", "tone"]
        )

    def _preprocess_input(self, raw_input: str) -> str:
        """Clean and standardize input text"""
        # Remove extra whitespace and normalize line endings
        cleaned = re.sub(r'\s+', ' ', raw_input).strip()
        # Convert common variations of section identifiers
        cleaned = re.sub(r'(?i)context\s*[:|-]', 'Context:', cleaned)
        cleaned = re.sub(r'(?i)tone\s*[:|-]', 'Tone:', cleaned)
        cleaned = re.sub(r'(?i)purpose\s*[:|-]', 'Purpose:', cleaned)
        return cleaned

    def _extract_tone(self, text: str) -> str:
        """Extract tone from input or return default"""
        tone_match = re.search(r'(?i)tone\s*[:|-]\s*([^.\n]+)', text)
        return tone_match.group(1).strip() if tone_match else self.default_tone

    async def process_input(self, raw_input: str) -> dict:
        """Process raw input into structured format with enrichment"""
        try:
            # Preprocess input
            cleaned_input = self._preprocess_input(raw_input)
            
            # Structure the input using LLM
            structure_chain = LLMChain(llm=self.llm, prompt=self.structure_prompt)
            structured_output = structure_chain.run(raw_input=cleaned_input)
            
            # Parse the structured output
            processed_data = self.output_parser.parse(structured_output)
            
            # Get enrichment based on structured data
            enrichment_chain = LLMChain(llm=self.llm, prompt=self.enrichment_prompt)
            enrichment = enrichment_chain.run(
                structured_data=str(processed_data.dict()),
                tone=processed_data.tone
            )
            
            # Combine original structure with enrichment
            final_output = {
                "structured_data": processed_data.dict(),
                "enrichment": enrichment,
                "metadata": {
                    "processed_at": datetime.now().isoformat(),
                    "model_used": self.llm.model
                }
            }
            
            return final_output
            
        except Exception as e:
            raise Exception(f"Error processing input: {str(e)}")

    def validate_output(self, output: dict) -> bool:
        """Validate the processed output"""
        try:
            required_fields = ["context", "tone", "purpose"]
            structured_data = output.get("structured_data", {})
            
            # Check for required fields
            for field in required_fields:
                if not structured_data.get(field):
                    return False
            
            # Validate lists are non-empty
            list_fields = ["key_points", "related_topics", "suggested_actions"]
            for field in list_fields:
                if not isinstance(structured_data.get(field), list) or \
                   not structured_data.get(field):
                    return False
            
            return True
            
        except Exception:
            return False