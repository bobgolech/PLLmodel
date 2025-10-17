"""
run.py — zero-setup launcher
- Creates a local venv at ./.venv (if missing)
- Installs requirements.txt into that venv (if missing)
- Runs main.py using the venv's Python
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
VENV_DIR = REPO_ROOT / ".venv"

def venv_python() -> Path:
    if platform.system() == "Windows":
        return VENV_DIR / "Scripts" / "python.exe"
    else:
        return VENV_DIR / "bin" / "python"

def ensure_venv():
    if not VENV_DIR.exists():
        print("Creating virtual environment (.venv)...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
    py = venv_python()
    if not py.exists():
        raise RuntimeError("Virtual environment looks broken; delete .venv and try again.")
    return py

def pip_install(py: Path):
    req = REPO_ROOT / "requirements.txt"
    if not req.exists():
        return  # no requirements, nothing to install
    print("Installing dependencies (this happens only once)...")
    # Upgrade pip (quietly), then install
    subprocess.check_call([str(py), "-m", "pip", "install", "--upgrade", "pip", "wheel"])
    subprocess.check_call([str(py), "-m", "pip", "install", "-r", str(req)])

def run_app(py: Path):
    main = REPO_ROOT / "main.py"
    if not main.exists():
        print("Error: main.py not found next to run.py")
        sys.exit(1)
    # Forward any args passed to run.py to main.py
    args = [str(py), str(main), *sys.argv[1:]]
    return subprocess.call(args)

def main():
    try:
        py = ensure_venv()
        # Check whether the needed packages are installed by trying to import quickly
        # If import fails, run pip install.
        need_install = False
        reqs = (REPO_ROOT / "requirements.txt").read_text().splitlines() if (REPO_ROOT / "requirements.txt").exists() else []
        reqs = [r.split("#", 1)[0].strip() for r in reqs if r.strip() and not r.strip().startswith("#")]
        if reqs:
            # Try importing a few top-level packages (best-effort)
            test_code = ";".join([f"import {r.split('==')[0].split('>=')[0].split('[')[0].replace('-', '_')}" for r in reqs])
            rc = subprocess.call([str(py), "-c", test_code], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            need_install = rc != 0
        if need_install:
            pip_install(py)
        sys.exit(run_app(py))
    except subprocess.CalledProcessError as e:
        print("\n❌ A command failed:\n", e)
        print("Tip: delete the .venv folder and run again.")
        sys.exit(1)
    except Exception as e:
        print("\n❌ Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()

    