import boto3
import json
from typing import Dict, List, Optional, Any
from botocore.exceptions import ClientError


class BedrockRetrieveAndGenerate:
    """
    A client for AWS Bedrock RetrieveAndGenerate API operations.
    """

    def __init__(self, region_name: str = 'us-east-1'):
        self.client = boto3.client('bedrock-agent-runtime', region_name=region_name)

    def basic_query(self, 
                   query: str, 
                   knowledge_base_id: str, 
                   model_arn: str = "Nova Pro") -> Dict:
        request_body = {
            "input": {
                "text": query
            },
            "retrieveAndGenerateConfiguration": {
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": knowledge_base_id,
                    "modelArn": model_arn
                },
                "type": "KNOWLEDGE_BASE"
            }
        }

        try:
            response = self.client.retrieve_and_generate(**request_body)
            return response
        except ClientError as e:
            print(f"Error: {e}")
            return None

    def print_response(self, response: Dict):
        """
        Print only the generated answer text from the API response.
        """
        if not response:
            print("No response received")
            return

        output_text = response.get('output', {}).get('text', 'No answer generated')
        print(output_text)


def main():
    """
    Example usage of the BedrockRetrieveAndGenerate class.
    """
    # Initialize the client
    client = BedrockRetrieveAndGenerate(region_name='us-east-1')

    # Replace with your actual knowledge base ID and model ARN
    knowledge_base_id = "2XEBWENGEO"
    model_arn = "amazon.nova-pro-v1:0"

    # Query
    response = client.basic_query(
        query="How many months of data is available for Allison Hill",
        knowledge_base_id=knowledge_base_id,
        model_arn=model_arn
    )

    # Print only the answer
    client.print_response(response)


if __name__ == "__main__":
    main()
