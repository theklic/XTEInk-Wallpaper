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

## Requirements

- Python 3.6 or higher
- Pillow library

Install Pillow with:
```
pip install Pillow
```

## How to Use

1. Run the converter:
   ```
   python converter.py
   ```

2. Place your images in the `input` folder (created automatically next to the script)

3. Click the **Convert** button

4. Find your converted images in the `output` folder

## Folder Structure

```
XTEInk-Wallpaper/
    converter.py
    README.md
    input/         <- Put your images here
    output/        <- Converted images appear here
```

## Notes

- If a file with the same name already exists in the output folder, the new file will be renamed with a suffix (e.g., `photo_1.bmp`)
- The input and output folders are created automatically when you run the program
- Progress is shown while converting multiple images
