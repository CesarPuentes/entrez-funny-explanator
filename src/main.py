from app import call_llm

def gcp_handler(request):
    """
    Cloud Function handler for Google Cloud Platform.
    GCP Cloud Functions (Gen 1) specifically looks for a file named `main.py`.
    """
    request_json = request.get_json(silent=True)
    gene = request_json.get("gene", "TP53") if request_json else "TP53"
    result = call_llm(gene)
    return result
