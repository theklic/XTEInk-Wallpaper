"""
XTEInk Wallpaper Converter

Converts images to 480x800 8-bit grayscale BMP format for XTEInk X4 devices.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox
import webbrowser
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


# Constants
OUTPUT_WIDTH = 480
OUTPUT_HEIGHT = 800
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif', '.webp'}


def get_app_directory():
    """Get the directory where the script/executable is located."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return Path(sys.executable).parent
    else:
        # Running as script
        return Path(__file__).parent.resolve()


def ensure_folders_exist(app_dir):
    """Create input and output folders if they don't exist."""
    input_folder = app_dir / "input"
    output_folder = app_dir / "output"

    input_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)

    return input_folder, output_folder


def get_unique_filename(output_folder, base_name):
    """Generate a unique filename if file already exists."""
    output_path = output_folder / f"{base_name}.bmp"

    if not output_path.exists():
        return output_path

    counter = 1
    while True:
        output_path = output_folder / f"{base_name}_{counter}.bmp"
        if not output_path.exists():
            return output_path
        counter += 1


def convert_image(image_path):
    """
    Convert an image to 480x800 8-bit grayscale BMP.

    Process:
    1. Resize height to 800 while maintaining aspect ratio
    2. If width > 480: center crop
    3. If width < 480: add white padding on sides
    """
    img = Image.open(image_path)

    # Convert to RGB first (handles various formats including RGBA, palette, etc.)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Calculate new dimensions (resize height to 800, maintain aspect ratio)
    original_width, original_height = img.size
    scale_factor = OUTPUT_HEIGHT / original_height
    new_width = int(original_width * scale_factor)
    new_height = OUTPUT_HEIGHT

    # Resize the image
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Handle width adjustment
    if new_width > OUTPUT_WIDTH:
        # Center crop
        left = (new_width - OUTPUT_WIDTH) // 2
        right = left + OUTPUT_WIDTH
        img = img.crop((left, 0, right, OUTPUT_HEIGHT))
    elif new_width < OUTPUT_WIDTH:
        # Add white padding on sides
        padded = Image.new('RGB', (OUTPUT_WIDTH, OUTPUT_HEIGHT), (255, 255, 255))
        paste_x = (OUTPUT_WIDTH - new_width) // 2
        padded.paste(img, (paste_x, 0))
        img = padded

    # Convert to 8-bit grayscale
    img = img.convert('L')

    return img


def get_image_files(input_folder):
    """Get list of supported image files in the input folder."""
    files = []
    for file_path in input_folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(file_path)
    return files


class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XTEInk Wallpaper Converter")
        self.root.resizable(False, False)

        # Get directories
        self.app_dir = get_app_directory()
        self.input_folder, self.output_folder = ensure_folders_exist(self.app_dir)

        # Build UI
        self.create_widgets()

        # Center window on screen
        self.center_window()

    def create_widgets(self):
        # Main frame with padding
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack()

        # Title
        title_label = tk.Label(
            main_frame,
            text="XTEInk Wallpaper Converter",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 15))

        # Convert button
        self.convert_btn = tk.Button(
            main_frame,
            text="Convert",
            command=self.run_conversion,
            width=20,
            height=2,
            font=('Arial', 11)
        )
        self.convert_btn.pack(pady=(0, 10))

        # Progress label
        self.progress_var = tk.StringVar()
        self.progress_var.set("")
        self.progress_label = tk.Label(
            main_frame,
            textvariable=self.progress_var,
            font=('Arial', 10)
        )
        self.progress_label.pack(pady=(0, 10))

        # Help link
        help_link = tk.Label(
            main_frame,
            text="Help",
            font=('Arial', 10, 'underline'),
            fg='blue',
            cursor='hand2'
        )
        help_link.pack()
        help_link.bind('<Button-1>', self.open_help)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def open_help(self, event=None):
        readme_path = self.app_dir / "README.md"
        if readme_path.exists():
            webbrowser.open(readme_path.as_uri())
        else:
            messagebox.showinfo("Help", "README.md not found.")

    def run_conversion(self):
        # Get image files
        image_files = get_image_files(self.input_folder)

        if not image_files:
            messagebox.showinfo(
                "No Images Found",
                f"The input folder is empty.\n\nPlace images in:\n{self.input_folder}"
            )
            return

        # Disable button during conversion
        self.convert_btn.config(state=tk.DISABLED)

        total = len(image_files)
        converted = 0
        errors = []

        for i, image_path in enumerate(image_files, 1):
            # Update progress
            self.progress_var.set(f"Processing {i}/{total}")
            self.root.update()

            try:
                # Convert the image
                converted_img = convert_image(image_path)

                # Get unique output filename
                base_name = image_path.stem
                output_path = get_unique_filename(self.output_folder, base_name)

                # Save as BMP
                converted_img.save(output_path, 'BMP')
                converted += 1

            except Exception as e:
                errors.append(f"{image_path.name}: {str(e)}")

        # Re-enable button
        self.convert_btn.config(state=tk.NORMAL)
        self.progress_var.set("")

        # Show results
        if errors:
            error_msg = "\n".join(errors[:5])  # Show first 5 errors
            if len(errors) > 5:
                error_msg += f"\n... and {len(errors) - 5} more errors"
            messagebox.showwarning(
                "Conversion Complete",
                f"Converted {converted}/{total} images.\n\nErrors:\n{error_msg}"
            )
        else:
            messagebox.showinfo(
                "Conversion Complete",
                f"Successfully converted {converted} image(s).\n\nOutput folder:\n{self.output_folder}"
            )


def main():
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
