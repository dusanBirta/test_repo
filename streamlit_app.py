import streamlit as st
import cv2
import numpy as np

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

        # Display the captured image
        st.image(image, channels="BGR", use_column_width=True)

if __name__ == '__main__':
    main()
