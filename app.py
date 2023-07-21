import streamlit as st
import cv2
import numpy as np

def main():
    st.title("Mouse Hover App")

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image using OpenCV
        image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image, 1)

        # Convert the image to RGB (OpenCV uses BGR by default, but Streamlit expects RGB)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Display the image with mouse hover text
        st.image(image_rgb, use_column_width=True, caption="Mouse hover")

if __name__ == "__main__":
    main()
