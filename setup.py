#!/usr/bin/env python3
"""
Algorzen Vigil - Setup and Installation Script
Algorzen Research Division © 2025 — Author Rishi Singh
"""

import sys
import subprocess
import os

def print_banner():
    """Print setup banner."""
    print("=" * 70)
    print("🧠 Algorzen Vigil - Setup & Installation")
    print("Algorzen Research Division © 2025 — Author Rishi Singh")
    print("=" * 70)
    print()

def check_python_version():
    """Check if Python version is 3.10+."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python 3.10+ required. Found: {version.major}.{version.minor}")
        print("   Please upgrade Python and try again.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required packages."""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    print("\nSetting up environment configuration...")
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from template")
            print("   Edit .env to add your OPENAI_API_KEY (optional)")
        else:
            print("⚠️  .env.example not found")
    else:
        print("✅ .env file already exists")

def run_test():
    """Run a test analysis."""
    print("\nRunning test analysis...")
    try:
        subprocess.check_call([
            sys.executable, "main.py",
            "--input", "data/sample_kpi_data.csv"
        ])
        print("\n✅ Test analysis completed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Test analysis failed")
        return False

def main():
    """Main setup function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Ask user if they want to run test
    print("\n" + "=" * 70)
    response = input("Would you like to run a test analysis? (y/n): ").lower()
    
    if response == 'y':
        success = run_test()
        if success:
            print("\n" + "=" * 70)
            print("✨ Setup Complete!")
            print("=" * 70)
            print("\nNext steps:")
            print("1. Review generated report in reports/ directory")
            print("2. Edit .env to add OPENAI_API_KEY (optional)")
            print("3. Run: python main.py --input your_data.csv")
            print("4. Or launch web UI: streamlit run app/streamlit_app.py")
            print("\n" + "=" * 70)
    else:
        print("\n" + "=" * 70)
        print("✨ Setup Complete!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Edit .env to add OPENAI_API_KEY (optional)")
        print("2. Run: python main.py --input data/sample_kpi_data.csv")
        print("3. Or launch web UI: streamlit run app/streamlit_app.py")
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
