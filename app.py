import streamlit as st
from ultralytics import YOLO
from PIL import Image
import cv2
import os

# Real-ESRGAN enhancement function
def enhance_image(input_image_path, output_image_path):
    # Enhance the image with Real-ESRGAN
    os.system(f'/home/appuser/venv/bin/python Real-ESRGAN/inference_realesrgan.py -n RealESRGAN_x4plus -i {input_image_path} --outscale 3.5 --face_enhance')

    # Check if the enhanced image is saved
    if not os.path.exists(output_image_path):
        st.error(f"Enhanced image not found at {output_image_path}")
        return None

    # Read the enhanced image
    enhanced_image = cv2.imread(output_image_path)
    if enhanced_image is None:
        st.error(f"Failed to read enhanced image from {output_image_path}")
        return None

    enhanced_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB)
    return enhanced_image

# Main app
st.title('Face Detection using YOLOv8 and Real-ESRGAN Enhancement')
st.subheader('Upload an image to perform face detection and enhancement')

# Upload image
uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:
    # Read the uploaded image
    uploaded_image = Image.open(uploaded_file)
    image_path = f'image_uploaded.{uploaded_file.type.split("/")[-1]}'
    uploaded_image.save(image_path)

    # Load YOLO model
    model = YOLO('yolov8n-face.pt')

    # Predict with the model
    results = model(image_path)

    # Load the original image
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Iterate through the detection results
    for result in results:
        # Get bounding box coordinates in the xyxy format
        xyxy_boxes = result.boxes.xyxy

        # Crop and enhance each bounding box
        for xyxy_box in xyxy_boxes:
            # Convert the bounding box coordinates to integers
            x1, y1, x2, y2 = map(int, xyxy_box)

            # Crop the image using the bounding box coordinates
            cropped_image = original_image[y1:y2, x1:x2]
            cropped_image_path = f'cropped_face.jpg'
            cv2.imwrite(cropped_image_path, cropped_image)

            # Enhance the cropped face image
            enhanced_image_path = 'Real-ESRGAN/results/cropped_face_out.jpg'
            enhanced_image = enhance_image(cropped_image_path, enhanced_image_path)

            # Show the original and enhanced face images in Streamlit
            st.image([cropped_image, enhanced_image], caption=['Original Face', 'Enhanced Face'])
