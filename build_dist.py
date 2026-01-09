import os
import subprocess
import sys

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.check_call(cmd, shell=True)

if __name__ == "__main__":
    # 1. Create a clean virtual environment
    run("python -m venv build_env")
    # 2. Activate venv and install only essential dependencies
    if os.name == "nt":
        activate = ".\\build_env\\Scripts\\activate"
    else:
        activate = "source build_env/bin/activate"
    run(f"{activate} && pip install --upgrade pip")
    run(f"{activate} && pip install nuitka")
    # 3. Install your minimal requirements (edit as needed)
    run(f"{activate} && pip install numpy onnxruntime")
    # 4. Bundle with Nuitka (edit run.py to your entry point)
    run(f"{activate} && nuitka --onefile --noconsole --include-data-dir=models=models run.py")
    print("\nBuild complete! Your standalone .exe is in the current directory.\n")
