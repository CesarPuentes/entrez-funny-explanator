# Entrez-Funny-Explanator

## Sample output:

```json
{
  "gene_name": "TP53",
  "biological_function": "Tumor suppressor that regulates cell cycle arrest, apoptosis, senescence, DNA repair, and metabolism in response to cellular stress.",
  "associated_diseases": ["Li-Fraumeni syndrome", "Various human cancers"],
  "layman_summary": "Think of this gene as the 'no-returns policy' enforcer of a cell: it checks if a cell is damaged and forces it to either repair or shut down to prevent chaos. When it's broken, cells can turn into troublemakers (cancer)."
}
```

## 🧬 Overview
Get explanations of what a gene does in a funny way. This project bridges the gap between **Bioinformatics** and **AI Engineering**.
It automates clinical research for a given human gene by fetching data from the US government's public API (NCBI) and passing it to an LLM (DeepSeek) to analyze, summarize, and structure the dense scientific data. 

The application returns a standardized JSON object ready to be consumed by a frontend or medical application.

## 🚀 Technical Requirements
* **Python 3.10+** (managed with `uv` recommended)
* `biopython`: To connect with NCBI Entrez.
* `openai`: Official client to query DeepSeek.
* `pydantic` (Optional): To enforce strict JSON typings.
* `terraform`: For cloud deployment infrastructure.

## 🛠️ Setup Instructions

This project recommends using [**`uv`**](https://github.com/astral-sh/uv) (a fast Python package manager) to manage the virtual environment and dependencies.

### 1. Initialize Virtual Environment with `uv`
Set up your environment and dependencies from the root folder:

```bash
# Create a virtual environment
uv venv

# Activate it
source .venv/bin/activate

# Install dependencies
uv pip install -r src/requirements.txt
```

*(Alternatively, using standard python: `python -m venv .venv && source .venv/bin/activate && pip install -r src/requirements.txt`)*

### 2. Local Configuration
We have included a setup script to streamline the environment configuration. Run it using `uv` (or `python`):

```bash
cd src
uv run install.py
```
*   You will be prompted for your **DeepSeek API Key** and your **NCBI Entrez Email**.
*   You will be asked to choose a deployment target (**AWS**, **GCP**, or **Local Only**).
*   If you choose a cloud provider, it will automatically generate a `.env` file (for local testing) and a `terraform.tfvars` file (for cloud deployment).
*   If you choose Local Only, it will skip the Terraform configuration and strictly set up your `.env` file for local execution.

### 3. Local Execution
You can run the script locally to test the integration using `uv` (or `python`):

```bash
cd src
uv run app.py
```

### 4. Cloud Deployment (AWS / GCP)
Once you confirm that the local execution works, you can deploy it to the cloud.

#### Preparing the Code
The application logic lives in `src/app.py` to keep it readable, while cloud-specific deployment handlers have been separated:
- **AWS**: Handled by `src/aws_handler.py`.
- **GCP**: Handled by `src/main.py` (GCP Gen 1 strictly requires `main.py` as the entry point).

The project is already configured to execute correctly on either platform out-of-the-box!

**Note on Clean Dependency Packaging (No Directory Pollution):**
*   **AWS (Lambda)**: The setup script uses a temporary build directory (`build`). It copies only the necessary Python code and automatically installs package requirements there (using `uv` if available, falling back to `pip`) before zipping.
*   **GCP (Cloud Functions)**: GCP builds your function natively on the cloud using `src/requirements.txt`. No local package installations are required for deploying.

#### Deploying with Terraform

**🐳 Docker Setup for Terraform**
If you don't have Terraform installed locally and want to use Docker, set up this exact alias in your terminal profile (e.g. `~/.bashrc`) before starting:
```bash
alias terraform='docker run --rm -it -v $(pwd):/workspace -w /workspace hashicorp/terraform:latest'
```
*Note: If you use this alias, you MUST run all `terraform` commands from inside the `src/` directory so the container can mount and access the build files.*
Initialize and apply the Terraform configuration for your chosen provider.

The setup script `install.py` will automatically prepare the `main.tf` file for your chosen provider. However, if you are setting this up manually, you can simply copy the correct template:

**For AWS:**
```bash
cd src
cp terraform_templates/aws.tf.tmpl main.tf
terraform init
terraform apply
```

**For GCP:**
```bash
cd src
cp terraform_templates/gcp.tf.tmpl main.tf
terraform init
terraform apply
```

### 🧪 Testing the Cloud Deployment
After running `terraform apply`, Terraform will output a `function_url` in your terminal. You can test your live cloud function using `curl` by sending a JSON payload.

*(Note: Depending on your specific Cloud configuration, the URL may still need to be generated manually from the AWS/GCP consoles and configured accordingly before it is publicly accessible.)*

```bash
# Replace <YOUR_FUNCTION_URL> with the output provided by Terraform (or your manual Console URL)
curl -X POST -H "Content-Type: application/json" \
     -d '{"gene": "BRCA1"}' \
     <YOUR_FUNCTION_URL>
```

### 🤖 CI/CD with GitHub Actions
This project includes automated deployment workflows via GitHub Actions!
They are located in the `.github/workflows/` directory.

To use them, you must configure the following **Secrets** in your GitHub repository settings (`Settings -> Secrets and variables -> Actions`):

#### Common Secrets
*   `DEEPSEEK_API_KEY`: Your DeepSeek API key.
*   `ENTREZ_EMAIL`: An email address to identify your requests to NCBI Entrez.

#### If deploying to AWS:
*   `AWS_ACCESS_KEY_ID`: Your AWS Access Key.
*   `AWS_SECRET_ACCESS_KEY`: Your AWS Secret Access Key.

#### If deploying to GCP:
*   `GCP_PROJECT_ID`: Your Google Cloud Project ID.
*   `GCP_SA_KEY`: The complete JSON content of your GCP Service Account (with Editor or Cloud Functions Admin permissions).
