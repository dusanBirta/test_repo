import streamlit as st
import numpy as np
import cv2
import gdown
from ultralytics import YOLO
from PIL import Image
import imageio
from skimage.transform import resize
from demo import load_checkpoints, make_animation
from skimage import img_as_ubyte
import os
import ffmpeg

# Title
st.title('Face Animation using YOLOv8 and First Order Motion Model')
st.subheader('Due to streamlit only having CPU access, processing may take in excess of 5 minutes to complete')
st.subheader('Upload an image to perform face animation')

# Function to play video
def play_video(video_path):
    video_file = open(video_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

# Download the pre-trained model
model_path = 'vox-adv-cpk.pth.tar'
if not os.path.exists(model_path):
    gdown.download('https://drive.google.com/uc?id=1L8P-hpBhZi8Q_1vP2KlQ4N6dvlzpYBvZ', model_path, quiet=False)

# Upload image
uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'jpeg', 'png'])
if uploaded_file is not None:
    uploaded_image = Image.open(uploaded_file)
    image_path = f'image_uploaded.{uploaded_file.type.split("/")[-1]}'
    uploaded_image.save(image_path)

    # Load YOLO model
    model = YOLO('yolov8n-face.pt')
    results = model(image_path)

    # Process results
    for r in results:
        im_array = r.plot()  # Get BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # Convert to RGB PIL image
        st.image(im, caption="YOLO Prediction", use_column_width=True)  # Display prediction

        # Crop detected faces
        xyxy_boxes = r.boxes.xyxy.cpu().numpy()  # Convert tensor to NumPy array
        cropped_faces = [im_array[y1:y2, x1:x2, ::-1] for x1, y1, x2, y2 in xyxy_boxes.astype(int)] # Crop and convert to RGB

        # Display cropped faces
        for idx, face in enumerate(cropped_faces):
            st.image(face, caption=f"Cropped Face {idx + 1}", use_column_width=True)

        # Allow user to select which cropped image to animate
        selected_face_idx = st.selectbox('Select a face to animate:', range(len(cropped_faces)))
        source_image = resize(cropped_faces[selected_face_idx], (256, 256))[..., :3]

        # Driving video path
        driving_video_path = 'driving.mp4'

        reader = imageio.get_reader(driving_video_path)
        driving_video = [resize(frame, (256, 256))[..., :3] for frame in reader]

        # Load checkpoints
        generator, kp_detector = load_checkpoints(config_path='vox-256.yaml', checkpoint_path=model_path)

        # Generate animation
        predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)

        # Save animation
        animation_path = 'output.mp4'
        imageio.mimsave(animation_path, [img_as_ubyte(frame) for frame in predictions], fps=20)

        # Display animation
        play_video(animation_path)
