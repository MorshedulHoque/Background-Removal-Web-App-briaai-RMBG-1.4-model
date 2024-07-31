from flask import Flask, request, render_template, url_for
from transformers import pipeline
import os
from PIL import Image
from datetime import datetime
import piexif

app = Flask(__name__)

# Static subdirectories for uploaded and processed images
UPLOAD_FOLDER = os.path.join(app.static_folder, 'uploads')
PROCESSED_FOLDER = os.path.join(app.static_folder, 'processed')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def correct_image_orientation(image_path):
    img = Image.open(image_path)
    try:
        exif_dict = piexif.load(img.info['exif'])
        orientation = exif_dict['0th'].get(piexif.ImageIFD.Orientation, 1)
        if orientation == 3:
            img = img.rotate(180, expand=True)
        elif orientation == 6:
            img = img.rotate(270, expand=True)
        elif orientation == 8:
            img = img.rotate(90, expand=True)
        img.save(image_path, "JPEG", exif=img.info['exif'])
    except (KeyError, AttributeError, piexif.InvalidImageDataError):
        # If there's no EXIF data or it's invalid, do nothing
        pass

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            # Sanitize the original filename
            original_filename = file.filename.replace(" ", "_")
            # Generate a timestamp
            timestamp = int(datetime.now().timestamp())
            # Create a new filename with the timestamp
            new_filename = f"{timestamp}_{original_filename}"

            # Save the uploaded image
            file_path = os.path.join(UPLOAD_FOLDER, new_filename)
            file.save(file_path)

            # Correct the image orientation
            correct_image_orientation(file_path)

            # Convert PNG image to RGB format
            img = Image.open(file_path)
            img = img.convert('RGB')
            img.save(file_path)

            # Process the image to remove the background
            pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)
            pillow_mask = pipe(file_path, return_mask=True)
            pillow_image = pipe(file_path)  # Apply mask on input and return a pillow image

            # Define the processed file path with PNG extension and the new filename
            processed_filename = f"{timestamp}_{os.path.splitext(original_filename)[0]}_removed.png"
            processed_file_path = os.path.join(PROCESSED_FOLDER, processed_filename)
            
            # Save the processed image in PNG format
            pillow_image.save(processed_file_path)

            # Generate URLs for the uploaded and processed images
            uploaded_img_url = url_for('static', filename=f'uploads/{new_filename}')
            processed_img_url = url_for('static', filename=f'processed/{processed_filename}')

            # Render a template to display both images
            return render_template('show_images.html', uploaded_img_url=uploaded_img_url, processed_img_url=processed_img_url)
        else:
            return 'Only PNG and JPG files are allowed'

    return render_template('show_images.html')

if __name__ == '__main__':
    # Run the application on the local IP address
    app.run(host='0.0.0.0', port=5000, debug=True)
