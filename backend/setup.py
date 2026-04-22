#!/usr/bin/env python3
"""
Contract Analyzer Backend Setup Script

This script helps you set up the backend by:
1. Creating virtual environment
2. Installing dependencies
3. Downloading spaCy model
4. Creating necessary directories
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and report status"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✓ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(f"Error: {e}")
        return False

def main():
    backend_dir = Path(__file__).parent
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║        Contract Analyzer - Backend Setup                   ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Create virtual environment
    venv_path = backend_dir / "venv"
    if not venv_path.exists():
        if not run_command(
            f"python -m venv {venv_path}",
            "Creating Python virtual environment"
        ):
            return False
    else:
        print("\n✓ Virtual environment already exists")
    
    # Step 2: Activate virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = str(venv_path / "Scripts" / "activate.bat")
        pip_cmd = str(venv_path / "Scripts" / "pip")
    else:
        activate_cmd = f"source {venv_path / 'bin' / 'activate'}"
        pip_cmd = str(venv_path / "bin" / "pip")
    
    # Install dependencies
    if not run_command(
        f"{pip_cmd} install -r requirements.txt",
        "Installing Python dependencies"
    ):
        return False
    
    # Step 3: Download spaCy model
    if not run_command(
        f"{pip_cmd} install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl",
        "Downloading spaCy English model (en_core_web_sm)"
    ):
        print("\nℹ You can manually install the spaCy model with:")
        print(f"  {pip_cmd} install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl")
    
    # Step 4: Create necessary directories
    upload_dir = backend_dir / "uploads"
    upload_dir.mkdir(exist_ok=True)
    print(f"\n✓ Created uploads directory: {upload_dir}")
    
    # Step 5: Create .env file
    env_file = backend_dir / ".env"
    env_example = backend_dir / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print(f"\n✓ Created .env file from template")
        print(f"  File: {env_file}")
        print(f"  ⚠ Please review and update if needed")
    
    # Print final instructions
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║                   Setup Complete! ✓                        ║
    ╚════════════════════════════════════════════════════════════╝
    
    Next Steps:
    
    1. Activate virtual environment:
       {"venv\\Scripts\\activate" if sys.platform == "win32" else "source venv/bin/activate"}
    
    2. Review configuration in .env file
    
    3. Start the backend server:
       python -m app.main
    
    4. API will be available at:
       http://localhost:8000
    
    5. Access API documentation:
       http://localhost:8000/docs
    
    📝 API Endpoints:
       POST /analyze     - Analyze a contract PDF
       GET  /health      - Health check
       GET  /            - API info
    
    ✨ For more information, see README.md
    """)
    
    return True

if __name__ == "__main__":
    import shutil
    success = main()
    sys.exit(0 if success else 1)
