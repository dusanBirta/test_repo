from ultralytics import YOLO
import streamlit as st
import base64
from PIL import Image
import io
import cv2
import torch
import numpy as np

def main():
    st.title("YOLOv8 Predictions with Mouse Click App")

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image as bytes
        image = Image.open(uploaded_file)
        img_array = np.array(image)

        # Get image dimensions
        height, width = img_array.shape[:2]

        # Load custom YOLO model named "best.pt"
        model = YOLO('best.pt')

        # Make predictions using the uploaded image
        results = model(img_array)

        # Extract the first (and only) result from the list
        result = results[0]

        # Process the result
        boxes = result.boxes

        # Draw bounding boxes and labels
        for (x1, y1, x2, y2, conf, class_num) in boxes.data:
            label = result.names[int(class_num)]
            color = [int(c) for c in COLORS[int(class_num) % len(COLORS)]]
            cv2.rectangle(img_array, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)  # Increased thickness to 3
            cv2.putText(img_array, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)  # Increased font size and thickness

        # Convert the PIL Image to bytes
        is_success, img_buffer = cv2.imencode(".png", img_array)
        if is_success:
            img_bytes = img_buffer.tobytes()

        # Custom HTML template for the click event
        click_html = f"""
        <div style="position: relative; display: inline-block;">
            <img src="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" alt="Image" width="{width}" height="{height}">
        </div>
        <script>
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
                for (var key in descriptions) {{
                    var coords = key.split('-');
                    var distance = Math.sqrt((mouseX - coords[0]) ** 2 + (mouseY - coords[1]) ** 2);
                    if (distance <= 50) {{
                        messageDiv.innerHTML += '<p style="position: absolute; left: ' + coords[0] + 'px; top: ' + coords[1] + 'px; background-color: #555; color: #fff; border-radius: 6px; padding: 5px;">' + descriptions[key] + '</p>';
                    }}
                }}
            }}
        </script>
        <div id="message" style="position: absolute; top: 0; left: 0;"></div>
        """

        st.components.v1.html(click_html, height=height, scrolling=False)

# Define some colors for drawing bounding boxes
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (128, 128, 0), (0, 128, 128), (128, 0, 128)]

if __name__ == "__main__":
    main()
