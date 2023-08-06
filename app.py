import streamlit as st
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import os
#test

def enhance_image(input_image_path, output_image_path):
    # Enhance the image with Real-ESRGAN
    enhance_command = f"/home/adminuser/venv/bin/python -m inference_realesrgan -n RealESRGAN_x4plus -i ${input_image_path} --outscale 3.5 --face_enhance"
    os.system(enhance_command)

    # Read the enhanced image
    enhanced_image = cv2.imread(output_image_path)
    enhanced_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB)
    
    return enhanced_image

# Display title and instruction
st.title('Face Detection and Enhancement using YOLOv8 and Real-ESRGAN')
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

    # Show the results
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        st.image(im, caption='Detected faces')  # Show image in Streamlit

    # Load the original image
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Counter for the face images
    face_counter = 0

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

            # Save the cropped image
            cropped_image_path = f'cropped_face_{face_counter}.png'
            cv2.imwrite(cropped_image_path, cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))

            # Define the enhanced image path
            enhanced_image_path = cropped_image_path.replace('.png', '_out.jpg')

            # Enhance the cropped image
            enhanced_image = enhance_image(cropped_image_path, enhanced_image_path)

            # Convert enhanced image to PIL Image and show in Streamlit
            enhanced_pil_image = Image.fromarray(enhanced_image)
            st.image(enhanced_pil_image, caption=f'Enhanced Face {face_counter}')

            # Increment the face counter
            face_counter += 1
