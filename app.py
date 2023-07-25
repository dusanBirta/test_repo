from ultralytics import YOLO
import streamlit as st
import base64
import torch
from PIL import Image
import io
import tempfile
import os

def predict_with_yolov8(img_path):
    # Load YOLOv8 model with the weights file "best.pt" and using the provided command-line arguments
    model = YOLO(args=f"task=detect mode=predict model=best.pt source={img_path}")

    # Run inference on the image
    results = model()

    return results

def main():
    st.title("YOLOv8 Predictions with Mouse Click App")

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image as bytes
        img_bytes = uploaded_file.read()

        # Create a temporary file to save the uploaded image
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()

        # Save the image bytes to the temporary file
        with open(temp_file.name, "wb") as f:
            f.write(img_bytes)

        # Display the uploaded image
        st.image(img_bytes, use_column_width=True, caption="Uploaded Image")

        # Predict with YOLOv8 using the temporary file path
        results = predict_with_yolov8(temp_file.name)

        # Display YOLOv8 predictions
        if "pred" in results.names:
            st.image(results.pred[0].get_image(), use_column_width=True, caption="YOLOv8 Predictions")

        # Custom HTML template for the click event
        click_html = f"""
        <div style="position: relative; display: inline-block;">
            <img src="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" alt="Image" width="400" height="400"
                 onclick="handleClick(event)" onmousemove="handleMouseOver(event)">
        </div>
        <script>
            // Dictionary to store descriptions and coordinates
            var descriptions = {{}};

            function handleClick(event) {{
                var mouseX = event.clientX;
                var mouseY = event.clientY;
                var description = prompt("Enter a description for this area:");
                if (description) {{
                    descriptions[mouseX + '-' + mouseY] = description;
                }}
            }}

            function handleMouseOver(event) {{
                var mouseX = event.clientX;
                var mouseY = event.clientY;

                var messageDiv = document.getElementById('message');
                messageDiv.innerHTML = '';

                // Display descriptions for the hovered area
                for (var key in descriptions) {{
                    var coords = key.split('-');
                    var distance = Math.sqrt((mouseX - coords[0]) ** 2 + (mouseY - coords[1]) ** 2);
                    if (distance <= 50) {{  // Only display descriptions within a radius of 50 pixels
                        messageDiv.innerHTML += '<p style="position: absolute; left: ' + coords[0] + 'px; top: ' + coords[1] + 'px; background-color: #555; color: #fff; border-radius: 6px; padding: 5px;">' + descriptions[key] + '</p>';
                    }}
                }}
            }}
        </script>
        <div id="message" style="position: absolute; top: 0; left: 0;"></div>
        """

        # Display the custom HTML template for the click event
        st.components.v1.html(click_html, height=400, scrolling=False)

        # Remove the temporary file after processing
        os.remove(temp_file.name)

if __name__ == "__main__":
    main()
