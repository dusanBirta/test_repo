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

# Function to play video
def play_video(video_path):
    video_file = open(video_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

# Title
st.title('Face Animation using YOLOv8 and First Order Motion Model')
st.subheader('Upload an image to perform face animation')

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

    # Process results and crop detected face
    for r in results:
        im_array = r.plot()
        result = results[0]
        xyxy_boxes = result.boxes.xyxy
        x1, y1, x2, y2 = map(int, xyxy_boxes[0])
        cropped_image = im_array[y1:y2, x1:x2]

    # Correct the color channels
    cropped_image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)

    # Continue with animation
    source_image = resize(cropped_image_rgb, (256, 256))[..., :3]
    url = 'https://github.com/dusanBirta/Animate-Photos/raw/main/driving.mp4'
    driving_video_path = 'temp_driving_video.mp4'
    gdown.download(url, driving_video_path, quiet=False)
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
