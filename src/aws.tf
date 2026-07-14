
# =================================================================
# STEP 1: PROVIDER & VARIABLE CONFIGURATION
# - Set target cloud provider to AWS (region: us-east-1).
# - Declare sensitive 'deepseek_api_key' variable to securely pass 
#   credentials without printing them to the console during execution.
# =================================================================

# =================================================================
# STEP 2: CODE PACKAGING
# - Compress the local application folder into a deployable .zip file.
# - Used to track code modifications and trigger redeployments.
# =================================================================

# =================================================================
# STEP 3: SECURITY & IAM ROLES
# - Create an IAM Role allowing the AWS Lambda service to execute 
#   actions ('sts:AssumeRole' policy).
# - Attach basic execution permissions (AWSLambdaBasicExecutionRole) 
#   so the Lambda function can write output logs to CloudWatch.
# =================================================================

# =================================================================
# STEP 4: LAMBDA FUNCTION DEPLOYMENT
# - Deploy the Python 3.11 function using the zipped package.
# - Configure runtime, handler entry point, and increase timeout to 
#   30s (required for LLM/API response latency).
# - Use 'source_code_hash' to guarantee redeployment ONLY when 
#   the local Python code changes.
# - Safely inject the DeepSeek API Key as an environment variable.
# =================================================================


# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Declare the variable for the DeepSeek API key
variable "deepseek_api_key" {
  type        = string
  description = "DeepSeek API Key for the Lambda"
  sensitive   = true
}

# Create a clean build directory and install dependencies there to avoid polluting the src folder
resource "null_resource" "build_lambda" {
  triggers = {
    requirements = filesha256("${path.module}/requirements.txt")
    code_hash    = sha256(join("", [for f in fileset(path.module, "*.py") : filesha256("${path.module}/${f}")]))
  }

  provisioner "local-exec" {
    command = <<EOT
      rm -rf ${path.module}/../outputs/build
      mkdir -p ${path.module}/../outputs/build
      cp ${path.module}/*.py ${path.module}/../outputs/build/
      if command -v uv &> /dev/null; then
        uv pip install --system -r ${path.module}/requirements.txt -t ${path.module}/../outputs/build/
      else
        pip install -r ${path.module}/requirements.txt -t ${path.module}/../outputs/build/
      fi
    EOT
  }
}

# Compress the clean build folder
data "archive_file" "app_zip" {
  depends_on  = [null_resource.build_lambda]
  type        = "zip"
  source_dir  = "${path.module}/../outputs/build"
  output_path = "${path.module}/../outputs/app_function.zip"
}

# 2. Create an IAM Role so Lambda has permission to run and write logs
resource "aws_iam_role" "lambda_role" {
  name = "ai_script_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
      }
    ]
  })
}

# Attach basic execution policy (allows logging to CloudWatch)
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Declare the variable for the Entrez email
variable "entrez_email" {
  type        = string
  description = "Email for NCBI Entrez"
}

# 3. Create the Lambda Function
resource "aws_lambda_function" "ai_lambda" {
  filename         = data.archive_file.app_zip.output_path
  function_name    = "Entrez_Funny_Explanator"
  role             = aws_iam_role.lambda_role.arn
  handler          = "aws_handler.lambda_handler" # points to aws_handler.py -> lambda_handler
  runtime          = "python3.11"
  timeout          = 30 # Increase timeout to 30s as LLM API calls can take a while
  
  # Tracks file modifications so it only updates when the code actually changes
  source_code_hash = data.archive_file.app_zip.output_base64sha256

  # Securely pass variables to the Lambda
  environment {
    variables = {
      DEEPSEEK_API_KEY = var.deepseek_api_key
      ENTREZ_EMAIL     = var.entrez_email
    }
  }
}
