import os
import glob
import shutil
import cv2
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from ultralytics.engine.model import YOLO

# Real-ESRGAN enhancement function
def enhance_image(input_folder='upload', outscale=3.5):
    result_folder = 'results'
    if os.path.isdir(result_folder):
        shutil.rmtree(result_folder)
    os.mkdir(result_folder)

    # Run the Real-ESRGAN enhancement
    os.system(f'python Real-ESRGAN/inference_realesrgan.py -n RealESRGAN_x4plus -i {input_folder} --outscale {outscale} --face_enhance')

    # Display results
    input_list = sorted(glob.glob(os.path.join(input_folder, '*')))
    output_list = sorted(glob.glob(os.path.join(result_folder, '*')))
    for input_path, output_path in zip(input_list, output_list):
        img_input = cv2.imread(input_path)
        img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
        img_output = cv2.imread(output_path)
        img_output = cv2.cvtColor(img_output, cv2.COLOR_BGR2RGB)

        # You can modify this part to show the images in Streamlit instead of using plt
        st.image([img_input, img_output], caption=['Input image', 'Real-ESRGAN output'])

# Streamlit app
def main():
    st.title('YOLOv8 Face Detection & Real-ESRGAN Enhancement')
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
        st.write("")
        st.write("Classifying...")

        upload_folder = 'upload'
        if os.path.isdir(upload_folder):
            shutil.rmtree(upload_folder)
        os.mkdir(upload_folder)

        file_path = os.path.join(upload_folder, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Load YOLO model
        model = YOLO('yolov8n-face.pt')

        # Detect faces
        results = model(file_path)
        results.show() # You can modify this to show the result in Streamlit

        # Enhance detected faces using Real-ESRGAN
        enhance_image(input_folder=upload_folder)

if __name__ == '__main__':
    main()
