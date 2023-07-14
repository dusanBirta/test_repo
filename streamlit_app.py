import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Function to capture image from webcam
def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame

# Streamlit app
def main():
    # Set page title
    st.title("Image Capture")

    # Button to capture image
    if st.button("Capture Image"):
        # Capture the image
        image = capture_image()

        # Convert the color channels from BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert the captured image to PIL format
        pil_image = Image.fromarray(rgb_image)

        # Display the captured image
        st.image(pil_image, channels="RGB", use_column_width=True)

if __name__ == '__main__':
    main()
