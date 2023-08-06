import streamlit as st
from ultralytics import YOLO
from PIL import Image
import cv2
import os
import shutil
import subprocess

# YOLO face detection
st.title("Face Detection and Enhancement")
uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    # Convert the file to an opencv image.
    image = Image.open(uploaded_file)
    image_path = "input_image.jpg"
    image.save(image_path)
    model = YOLO('yolov8n-face.pt')
    results = model(image_path)
    im_array = results.render()[0]  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    st.image(im, caption="Detected faces")

    face_counter = 0
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    for result in results:
        xyxy_boxes = result.boxes.xyxy
        for xyxy_box in xyxy_boxes:
            x1, y1, x2, y2 = map(int, xyxy_box)
            cropped_image = original_image[y1:y2, x1:x2]
            face_path = f'face_{face_counter}.jpg'
            cv2.imwrite(face_path, cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))
            st.image(face_path, caption=f"Face {face_counter}")

            # Enhance the face image using Real-ESRGAN
            # Assuming Real-ESRGAN repository is cloned and set up properly
            upload_folder = 'Real-ESRGAN/upload'
            result_folder = 'Real-ESRGAN/results'
            if os.path.isdir(upload_folder):
                shutil.rmtree(upload_folder)
            if os.path.isdir(result_folder):
                shutil.rmtree(result_folder)
            os.mkdir(upload_folder)
            os.mkdir(result_folder)
            dst_path = os.path.join(upload_folder, face_path)
            shutil.move(face_path, dst_path)
            subprocess.run(['python', 'Real-ESRGAN/inference_realesrgan.py', '-n', 'RealESRGAN_x4plus', '-i', upload_folder, '--outscale', '3.5', '--face_enhance'])
            enhanced_face_path = os.path.join(result_folder, face_path)
            st.image(enhanced_face_path, caption=f"Enhanced Face {face_counter}")
            face_counter += 1
