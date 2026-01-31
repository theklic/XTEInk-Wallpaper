"""
Build script to create a standalone .exe using PyInstaller.

Requirements:
    pip install pyinstaller pillow

Usage:
    python build.py
"""

import subprocess
import sys


def main():
    # PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',           # Single .exe file
        '--windowed',          # No console window
        '--name', 'XTEInk Wallpaper Converter',
        'converter.py'
    ]

    print("Building executable...")
    print(f"Running: {' '.join(cmd)}\n")

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\nBuild complete!")
        print("Executable is in the 'dist' folder.")
    else:
        print("\nBuild failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
