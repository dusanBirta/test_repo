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

        # Convert the middle section to base64 to be used in the tooltip
        _, encoded_middle_section = cv2.imencode(".png", middle_section)
        middle_section_base64 = encoded_middle_section.tobytes()

        # Custom HTML template for the tooltip
        tooltip_html = f"""
        <div style="position: relative; display: inline-block;">
            <img src="data:image/png;base64,{middle_section_base64}" alt="Image" width="400" height="400"
                 onmouseover="showText(event)" onmouseout="hideText(event)">
            <div id="tooltip" style="visibility: hidden; width: 150px; background-color: #555; color: #fff;
                        text-align: center; border-radius: 6px; padding: 5px; position: absolute;
                        z-index: 1; bottom: 120%; left: 50%; margin-left: -75px;">
            </div>
        </div>
        <script>
            function showText(event) {{
                var tooltip = document.getElementById('tooltip');
                var image = event.target;
                var mouseX = event.offsetX;
                var imageWidth = image.clientWidth;
                if (mouseX < imageWidth / 2) {{
                    tooltip.innerHTML = 'Left';
                }} else {{
                    tooltip.innerHTML = 'Right';
                }}
                tooltip.style.visibility = 'visible';
            }}
            function hideText(event) {{
                var tooltip = document.getElementById('tooltip');
                tooltip.style.visibility = 'hidden';
            }}
        </script>
        """

        # Display the image with the tooltip
        st.components.v1.html(tooltip_html, height=400, scrolling=False)

if __name__ == "__main__":
    main()
