import streamlit as st
import cv2
import numpy as np
from streamlit import components

# Function to get the middle section of the image
def get_middle_section(image):
    height, width, _ = image.shape
    middle_x, middle_y = int(width / 2), int(height / 2)
    return image[middle_y - 50 : middle_y + 50, middle_x - 50 : middle_x + 50]

# Custom HTML template for the tooltip
def custom_html(image_bytes, tooltip_text):
    return f"""
    <div style="position: relative; display: inline-block;">
        <img src="data:image/png;base64,{image_bytes}" alt="Image" width="400" height="400">
        <div style="visibility: hidden; width: 150px; background-color: #555; color: #fff;
                    text-align: center; border-radius: 6px; padding: 5px; position: absolute;
                    z-index: 1; bottom: 120%; left: 50%; margin-left: -75px;"
            onmouseover="this.style.visibility='visible';"
            onmouseout="this.style.visibility='hidden';"
        >
            {tooltip_text}
        </div>
    </div>
    """

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

        # Convert the middle section to base64 to be used in the tooltip
        _, encoded_middle_section = cv2.imencode(".png", middle_section)
        middle_section_base64 = encoded_middle_section.tobytes()

        # Call the function to display the image with the tooltip
        tooltip_text = "Mouse Writing."
        st.components.v1.html(custom_html(middle_section_base64, tooltip_text))

if __name__ == "__main__":
    main()
