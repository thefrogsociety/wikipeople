import shutil
import os
import sys

DEPLOY_REPO_NAME = 'projects'
APP_SUBDIR = 'wikipeople'
DEPLOY_ROOT = os.path.join('..', DEPLOY_REPO_NAME) 
FINAL_TARGET = os.path.join(DEPLOY_ROOT, APP_SUBDIR) 
SRC_DATA = 'full_graph.json'
SRC_APP_FILE = os.path.join('wikipeople', 'index.html')


def copy_files():
    """Copies all necessary files into the target deployment repository."""
    
    print("--- Starting WikiPeople Deployment Build ---")
    
    if not os.path.isdir(DEPLOY_ROOT):
        print(f"Error: Deployment target directory '{DEPLOY_ROOT}' not found.")
        print("Please ensure the 'projects' repository is cloned next to this folder.")
        sys.exit(1)
        
    if not os.path.exists(SRC_DATA):
        print(f"Error: Data file '{SRC_DATA}' not found. Run 'python create_full_json.py'.")
        sys.exit(1)


    os.makedirs(FINAL_TARGET, exist_ok=True)

    print(f"Copying live files to {FINAL_TARGET}...")
    
    shutil.copy2(SRC_APP_FILE, FINAL_TARGET)

    shutil.copy2(SRC_DATA, FINAL_TARGET)
    
    if os.path.exists('_redirects'):
        shutil.copy2('_redirects', DEPLOY_ROOT)
        print(f"Copied _redirects file to {DEPLOY_ROOT} root.")


    print("\n✅ Build complete. Ready to commit the 'projects' repository.")

if __name__ == "__main__":
    copy_files()
