import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from Bio import Entrez

# 1. Load local .env file if it exists
load_dotenv()

Entrez.email = os.environ.get("ENTREZ_EMAIL", "default@example.com")

def fetch_gene_summary(gene_name: str) -> str:
    # Search for the gene ID
    handle = Entrez.esearch(db="gene", term=f"{gene_name}[Gene Name] AND human[Organism]")
    record = Entrez.read(handle)
    handle.close()

    if not record["IdList"]:
        return ""
        
    gene_id = record["IdList"][0]

    # Fetch clinical/biological summary using the ID
    handle = Entrez.esummary(db="gene", id=gene_id)
    summary = Entrez.read(handle)
    handle.close()
    
    try:
        final_summary = summary["DocumentSummarySet"]["DocumentSummary"][0]["Summary"]
        return final_summary
    except (KeyError, IndexError):
        return ""


def call_llm(gene: str) -> str:
    gene_info = fetch_gene_summary(gene)
    if not gene_info:
        return json.dumps({"error": f"No summary found for gene {gene}"})

    # Initialize client (It's better to pull the key here)
    client = OpenAI(
        # api_key=os.getenv("DEEPSEEK_API_KEY"),
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com" 
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system", 
                "content": (
                    f"You are a system specialized in bioinformatics. Analyze the following data: {gene_info}.\n\n"
                    "Provide a JSON response with exactly this structure:\n"
                    "{\n"
                    '  "gene_name": "Name of the gene",\n'
                    '  "biological_function": "Clear description of its cellular function",\n'
                    '  "associated_diseases": ["List", "of", "associated", "diseases"],\n'
                    '  "layman_summary": "Ultra-simple analogy in funny terms to explain it to a patient with no biology background"\n'
                    "}"
                )
            }
        ],
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content


# --- Execution ---
if __name__ == "__main__":
    result = call_llm("IL1A")
    print(result)