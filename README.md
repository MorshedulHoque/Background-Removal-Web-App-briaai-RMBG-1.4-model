# Background Removal Web App

This web application leverages the `briaai-RMBG-1.4` pretrained model to remove backgrounds from images. Built using Flask, it allows users to upload an image and view the results with a side-by-side comparison of the original and processed images.

## Features

- **Image Upload**: Users can upload an image for background removal.
  ![benchmark](https://github.com/MorshedulHoque/Background-Removal-Web-App-briaai-RMBG-1.4-model/blob/main/Screenshot_1.png)
- **Before and After Comparison**: View the original image alongside the processed image with the background removed.
  ![benchmark](https://github.com/MorshedulHoque/Background-Removal-Web-App-briaai-RMBG-1.4-model/blob/main/Screenshot_2.png)
- **Flask Backend**: The application is built using the Flask framework.
- **PIL for Image Processing**: Utilizes the Python Imaging Library (PIL) for image handling.
- **EXIF Data Handling**: Maintains the image's EXIF data using the `piexif` library.
- **Model Integration**: Uses the `briaai-RMBG-1.4` model from the `transformers` library.
