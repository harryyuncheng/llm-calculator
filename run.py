#!/usr/bin/env python3
"""
Setup and run script for the LLM Calculator
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        # For now, no dependencies are needed since we're using tkinter (built-in)
        # Uncomment below when ready to add anthropic API
        # subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All dependencies ready (using built-in tkinter)")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def run_calculator():
    """Run the calculator application"""
    print("Starting LLM Calculator...")
    try:
        subprocess.run([sys.executable, "calculator.py"])
    except KeyboardInterrupt:
        print("\nCalculator closed by user")
    except Exception as e:
        print(f"Error running calculator: {e}")

def main():
    """Main setup and run function"""
    print("LLM Calculator Setup")
    print("=" * 20)
    
    check_python_version()
    install_dependencies()
    
    print("\nSetup complete! Starting calculator...")
    print("Note: Currently using simulated Claude API. See calculator.py for real API integration.")
    print()
    
    run_calculator()

if __name__ == "__main__":
    main()
