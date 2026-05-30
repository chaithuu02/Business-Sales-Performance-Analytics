import os
import sys
import subprocess

def run_script(script_path):
    print("=" * 60)
    print(f"Running script: {script_path}")
    print("=" * 60)
    
    # Use the same python executable that is running this script
    cmd = [sys.executable, script_path]
    
    try:
        # Run process and stream output to console
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Read output line by line as it is generated
        for line in process.stdout:
            print(line, end="")
            
        process.wait()
        
        if process.returncode != 0:
            print(f"\nError: Script {script_path} failed with exit code {process.returncode}")
            sys.exit(process.returncode)
            
        print(f"\nSuccessfully finished: {script_path}\n")
    except Exception as e:
        print(f"\nFailed to execute {script_path}: {e}")
        sys.exit(1)

def main():
    # Ensure working directory is the project root (where run_pipeline.py is)
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    scripts = [
        "scripts/prepare_data.py",
        "scripts/export_js_data.py",
        "scripts/generate_notebook.py",
        "scripts/generate_pdf_report.py"
    ]
    
    for script in scripts:
        if not os.path.exists(script):
            print(f"Error: Script not found: {script}")
            sys.exit(1)
            
    print("Starting Business Sales Performance Analytics Pipeline...\n")
    
    for script in scripts:
        run_script(script)
        
    print("=" * 60)
    print("Pipeline Execution Completed Successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
