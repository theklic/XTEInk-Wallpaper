# XTEInk Wallpaper Converter

A simple utility to convert images to the format required by XTEInk X4 e-ink devices.

## What It Does

Converts your images to:
- **Size:** 480 x 800 pixels
- **Format:** BMP (8-bit grayscale)

The converter automatically:
- Resizes images to fit the height (800px)
- Center-crops if the image is too wide
- Adds white padding if the image is too narrow

## Supported Input Formats

- JPG / JPEG
- PNG
- BMP
- GIF
- TIFF
- WEBP

## How to Use

1. Place your images in the `input` folder (next to the program)
2. Run the converter (double-click the .exe or run the script)
3. Click the **Convert** button
4. Find your converted images in the `output` folder

## Folder Structure

```
XTEInk-Wallpaper/
    XTEInk Wallpaper Converter.exe   (or converter.py)
    README.md
    input/         <- Put your images here
    output/        <- Converted images appear here
```

## Notes

- The `input` and `output` folders are created automatically
- If a file already exists in output, the new file gets a suffix (e.g., `photo_1.bmp`)
- Progress is shown while converting multiple images

---

## Building the Executable

To build a standalone .exe that anyone can run without installing Python:

1. Install the build dependencies:
   ```
   pip install pyinstaller pillow
   ```

2. Run the build script:
   ```
   python build.py
   ```

3. Find the .exe in the `dist` folder

## Running from Source

If you prefer to run the Python script directly:

1. Install Pillow:
   ```
   pip install Pillow
   ```

2. Run:
   ```
   python converter.py
   ```
