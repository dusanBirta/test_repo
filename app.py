from ultralytics import YOLO
import streamlit as st
import base64
from PIL import Image
import io
import cv2
import numpy as np

def main():
    st.title("Snapdetect)

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image as bytes
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        height, width, _ = img_array.shape
        
        # Set display size
        display_width = min(width, 1000)
        display_height = int((display_width / width) * height)

        # Load custom YOLO model named "best.pt"
        model = YOLO('best.pt')  # Adjust the path if necessary

        # Make predictions using the uploaded image
        results = model(img_array)

        # Extract the first (and only) result from the list
        result = results[0]

        # Process the result
        boxes = result.boxes  # Boxes object for bbox outputs
        box_areas = []

        for (x1, y1, x2, y2, conf, class_num) in boxes.data:
            label = result.names[int(class_num)]
            color = [int(c) for c in COLORS[int(class_num) % len(COLORS)]]  # Choose a readable color based on the class
            cv2.rectangle(img_array, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(img_array, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            box_areas.append([x1, y1, x2, y2])

        # Convert the PIL Image to bytes
        is_success, img_buffer = cv2.imencode(".png", img_array)
        if is_success:
            img_bytes = img_buffer.tobytes()

        # Custom HTML template for the click event
        click_html = f"""
        <div style="position: relative; display: inline-block;">
            <img src="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" alt="Image" width="{display_width}" height="{display_height}" onclick="handleClick(event)" onmousemove="handleMouseOver(event)">
        </div>
        <script>
            var descriptions = {{}};
            var boxAreas = {box_areas};

            var scalingFactorWidth = {display_width} / {width};
            var scalingFactorHeight = {display_height} / {height};

            function adjustCoordinates(coord, isWidth) {{
                return isWidth ? coord * scalingFactorWidth : coord * scalingFactorHeight;
            }}

            function isInsideBox(mouseX, mouseY, box) {{
                return mouseX >= adjustCoordinates(box[0], true) && mouseX <= adjustCoordinates(box[2], true) && mouseY >= adjustCoordinates(box[1], false) && mouseY <= adjustCoordinates(box[3], false);
            }}

            function handleClick(event) {{
                var mouseX = event.clientX;
                var mouseY = event.clientY;
                
                for (var i = 0; i < boxAreas.length; i++) {{
                    if (isInsideBox(mouseX, mouseY, boxAreas[i])) {{
                        var description = prompt("Enter a description for this area:");
                        if (description) {{
                            descriptions[mouseX + '-' + mouseY] = description;
                        }}
                        break;
                    }}
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
        st.components.v1.html(click_html, height=display_height, scrolling=False)

# Define some readable colors for drawing bounding boxes
COLORS = [(128, 128, 128), (50, 168, 82), (50, 82, 168), (168, 168, 50), (50, 168, 132), (168, 50, 132), (80, 80, 0), (0, 80, 80), (80, 0, 80)]

if __name__ == "__main__":
    main()
