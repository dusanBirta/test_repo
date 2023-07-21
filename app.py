import streamlit as st
import cv2
import numpy as np

# Function to get the middle section of the image
def get_middle_section(image):
    height, width, _ = image.shape
    middle_x, middle_y = int(width / 2), int(height / 2)
    return image[middle_y - 50 : middle_y + 50, middle_x - 50 : middle_x + 50]

def main():
    st.title("Mouse Writing App")

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image using OpenCV
        image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image, 1)

        # Get the middle section of the image
        middle_section = get_middle_section(image)

        # Display the original image
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Show the tooltip text when hovering over the middle section of the image
        tooltip_text = "Mouse Writing."
        st.image(middle_section, caption="Middle Section", use_column_width=True)

        # Add a balloon tooltip to display the text when hovering over the middle section
        st.balloons()

if __name__ == "__main__":
    main()
