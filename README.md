# Background-Removal-Web-App-briaai-RMBG-1.4
 

# Background Removal Web App

This web application leverages the `briaai-RMBG-1.4` pretrained model to remove backgrounds from images. Built using Flask, it allows users to upload an image and view the results with a side-by-side comparison of the original and processed images.

## Features


- **Image Upload**: Users can upload an image for background removal.
- **Before and After Comparison**: View the original image alongside the processed image with the background removed.
- **Flask Backend**: The application is built using the Flask framework.
- **PIL for Image Processing**: Utilizes the Python Imaging Library (PIL) for image handling.
- **EXIF Data Handling**: Maintains the image's EXIF data using the `piexif` library.
- **Model Integration**: Uses the `briaai-RMBG-1.4` model from the `transformers` library.
