from app import call_llm

def lambda_handler(event, context):
    """
    Lambda function handler for AWS.
    """
    gene = event.get("gene", "TP53")
    result = call_llm(gene)
    return {
        "statusCode": 200,
        "body": result
    }
