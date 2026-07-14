
# =================================================================
# STEP 1: GCP PROVIDER & VARIABLES
# - Initialize Google Cloud Provider with Project ID and us-central1 region.
# - Declare sensitive variable for the DeepSeek API Key.
# =================================================================

# =================================================================
# STEP 2: CODE PACKAGING
# - Dynamically zip the local application source directory.
# =================================================================

# =================================================================
# STEP 3: CLOUD STORAGE SETUP (MANDATORY IN GCP)
# - Create a secure GCS Bucket to store the application code.
# - Upload the zipped package as a Bucket Object, appending its MD5 
#   hash to the name to force updates when the code changes.
# =================================================================

# =================================================================
# STEP 4: CLOUD FUNCTION DEPLOYMENT
# - Deploy the HTTP-triggered Cloud Function (equivalent to AWS Lambda).
# - Point the runtime source to the GCS Bucket Object created in Step 3.
# - Set runtime to Python 3.11 and define entry point handler.
# - Inject the DeepSeek API Key safely into the environment variables.
# =================================================================

# =================================================================
# STEP 5: ACCESS CONTROL & OUTPUTS
# - Assign the 'roles/cloudfunctions.invoker' IAM role to 'allUsers' 
#   to make the HTTP URL publicly accessible.
# - Output the generated Cloud Function URL for direct API testing.
# =================================================================

provider "google" {
  project = var.gcp_project_id
  region  = "us-central1"
}

variable "gcp_project_id" {
  type        = string
  description = "The ID of the Google Cloud project"
}

variable "deepseek_api_key" {
  type        = string
  description = "DeepSeek API Key"
  sensitive   = true
}

variable "entrez_email" {
  type        = string
  description = "Email for NCBI Entrez"
}

# Compress the code folder (Same as AWS)
data "archive_file" "function_zip" {
  type        = "zip"
  source_dir  = "${path.module}"
  output_path = "${path.module}/../outputs/gcp_function.zip"
}

# In GCP, it is MANDATORY to upload the zip to a Bucket first
resource "google_storage_bucket" "function_bucket" {
  name          = "${var.gcp_project_id}-gcf-source"
  location      = "US"
  force_destroy = true
}

resource "google_storage_bucket_object" "function_zip_object" {
  name   = "function-source-${data.archive_file.function_zip.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_zip.output_path
}

# Create the Cloud Function (Equivalent to Lambda)
resource "google_cloudfunctions_function" "ai_function" {
  name        = "entrez-funny-explanator"
  description = "Get explanations of what a gene does in a funny way."
  runtime     = "python311"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.function_zip_object.name
  trigger_http          = true # Makes it immediately invocable via a public URL
  entry_point           = "gcp_handler"

  environment_variables = {
    DEEPSEEK_API_KEY = var.deepseek_api_key
    ENTREZ_EMAIL     = var.entrez_email
  }
}

# IAM permission to invoke the function publicly via an HTTP URL
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.ai_function.project
  region         = google_cloudfunctions_function.ai_function.region
  cloud_function = google_cloudfunctions_function.ai_function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}

# After finishing, Terraform will output the URL
output "function_url" {
  value = google_cloudfunctions_function.ai_function.https_trigger_url
}
