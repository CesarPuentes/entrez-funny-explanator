import os
import shutil

def main():
    print("=== AI Engineer Capstone Project Teardown ===")
    print("This script will help you clean up your cloud resources and local generated files.")
    
    import subprocess
    
    print("\nSTEP 1: Cloud Teardown")
    if not os.path.exists("main.tf") or not os.path.exists("terraform.tfstate"):
        print("No active Terraform deployment found (missing main.tf or terraform.tfstate). Skipping cloud teardown.")
    else:
        confirm = input("⚠️ WARNING: This will permanently delete all cloud resources managed by the current configuration to avoid charges! Are you sure? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Teardown cancelled.")
            return
            
        print("\nDestroying resources...")
        
        # Check if terraform is installed natively, otherwise use the docker fallback
        if shutil.which("terraform"):
            cmd = ["terraform", "destroy", "-auto-approve"]
        else:
            print("(Terraform binary not found. Executing via Docker...)")
            cmd = [
                "docker", "run", "--rm", "-it",
                "-v", f"{os.getcwd()}:/workspace",
                "-w", "/workspace",
                "hashicorp/terraform:latest",
                "destroy", "-auto-approve"
            ]
            
        try:
            subprocess.run(cmd, check=True)
            print("✅ Cloud resources successfully destroyed.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to destroy cloud resources: {e}")
            print("Please fix the errors above before cleaning up local files.")
            return
        
    print("\nSTEP 2: Local Cleanup")
    files_to_remove = [
        "main.tf",
        "terraform.tfvars",
        ".env",
        "app_function.zip",
        "terraform.tfstate",
        "terraform.tfstate.backup",
        ".terraform.lock.hcl"
    ]
    
    dirs_to_remove = [
        "build",
        ".terraform"
    ]
    
    for f in files_to_remove:
        if os.path.exists(f):
            try:
                os.remove(f)
                print(f"🗑️ Deleted file: {f}")
            except Exception as e:
                print(f"⚠️ Could not delete {f}: {e}")
            
    for d in dirs_to_remove:
        if os.path.exists(d):
            try:
                shutil.rmtree(d)
                print(f"🗑️ Deleted directory: {d}")
            except PermissionError:
                print(f"⚠️ Permission denied deleting '{d}/'. This is likely because Docker created it as root. To force delete it, run: sudo rm -rf {d}")
            except Exception as e:
                print(f"⚠️ Could not delete directory {d}: {e}")
                
    print("\n✅ Local cleanup complete! Your environment is back to a clean state.")

if __name__ == "__main__":
    main()
