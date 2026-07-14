import os
import getpass

def main():
    print("=== AI Engineer Capstone Project Setup ===")
    deepseek_key = getpass.getpass("Enter your DeepSeek API Key: ")
    
    print("\nSelect your Cloud Provider:")
    print("1. AWS")
    print("2. GCP")
    print("3. Local Only (Skip Cloud Deployment)")
    
    choice = input("Enter choice (1/3): ").strip()
    
    aws_access_key = ""
    aws_secret_key = ""
    gcp_project_id = ""
    provider = ""

    entrez_email = input("Provide an email for NCBI Entrez: ").strip()
    if choice == "1":
        provider = "aws"
        aws_access_key = input("Enter AWS Access Key ID: ").strip()
        aws_secret_key = getpass.getpass("Enter AWS Secret Access Key: ").strip()
    elif choice == "2":
        provider = "gcp"
        gcp_project_id = input("Enter GCP Project ID: ").strip()
    elif choice == "3":
        provider = "local"
        print("Environment (.env) file will be generated to local installation. Skipping cloud installation. Have fun!")
    else:
        print("Invalid choice. Exiting.")
        return
        
    # Write .env file for local execution
    env_content = f"DEEPSEEK_API_KEY={deepseek_key}\n"
    env_content += f"ENTREZ_EMAIL={entrez_email}\n"
    if provider == "aws":
        env_content += f"AWS_ACCESS_KEY_ID={aws_access_key}\n"
        env_content += f"AWS_SECRET_ACCESS_KEY={aws_secret_key}\n"
    
    with open(".env", "w") as f:
        f.write(env_content)
        
    print("\n✅ .env file generated successfully.")
    
    if provider != "local":
        # Write terraform.tfvars for Terraform deployment
        tfvars_content = f'deepseek_api_key = "{deepseek_key}"\n'
        tfvars_content += f'entrez_email = "{entrez_email}"\n'
        if provider == "aws":
            tfvars_content += f'aws_access_key = "{aws_access_key}"\n'
            tfvars_content += f'aws_secret_key = "{aws_secret_key}"\n'
        elif provider == "gcp":
            tfvars_content += f'gcp_project_id = "{gcp_project_id}"\n'
            
        import shutil
        shutil.copy(f"terraform_templates/{provider}.tf.tmpl", "main.tf")
        
        with open("terraform.tfvars", "w") as f:
            f.write(tfvars_content)
            
        print("✅ terraform.tfvars generated successfully.")
        
        if provider == "aws":
            print("\nBuilding AWS Lambda package locally...")
            import os, subprocess
            os.makedirs("build", exist_ok=True)
            for file in os.listdir("."):
                if file.endswith(".py"):
                    shutil.copy(file, "build/")
            try:
                # AWS Lambda runs Python 3.11, so we must explicitly tell uv to fetch 3.11 wheels
                # otherwise it fetches cp313 (Python 3.13) wheels which will crash Lambda with "No module named pydantic_core._pydantic_core"
                subprocess.run(["uv", "pip", "install", "--system", "--python", "3.11", "-r", "requirements.txt", "-t", "build/"], check=True)
            except FileNotFoundError:
                subprocess.run(["pip", "install", "-r", "requirements.txt", "-t", "build/"], check=True)
            print("✅ AWS Lambda package built successfully.")

        print("\nNext steps:")
        print("1. Cloud handlers are pre-configured in `aws_handler.py` and `main.py` (for GCP).")
        print("2. Run 'terraform init' and 'terraform apply'")
    else:
        print("\nNext steps:")
        print("Run 'python app.py' to start the application locally.")

if __name__ == "__main__":
    main()