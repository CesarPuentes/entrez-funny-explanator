import os
# AWS Lambda's filesystem is read-only except for /tmp.
# Biopython's Entrez module attempts to write a local DTD cache to the user's home directory.
# By overriding the HOME environment variable to /tmp, we force the cache to be written to the writable directory.
os.environ["HOME"] = "/tmp"

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
