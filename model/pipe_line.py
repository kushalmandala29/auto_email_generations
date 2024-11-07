# from model import reponse_modifier
from reponse_modifier import DataStructurer 


# from model import reponse_modifier


class EmailGenerationPipeline:
    def __init__(self):
        self.data_processor = DataStructurer()

    def process(self, input_data):
        processed_input = self.data_processor.structure_data(input_data)
        return processed_input
    
if __name__ == "__main__":
    # Example input data
    raw_input = """
Need to send update about the new product launch to stakeholders.
Include information about timeline and budget updates.
Make sure to highlight the key achievements so far.
"""

    # Initialize the data processor
    # data_processor = DataProcessor()

    # Create the email generation pipeline
    pipeline = EmailGenerationPipeline()

    # Process the input data
    # processed_input = pipeline.process(input_data)
    output = pipeline.process(raw_input)
    # Print the processed input
    print(output)