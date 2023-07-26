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

        # Convert the PIL Image to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        # Display the uploaded image
        #st.image(img_bytes, use_column_width=True, caption="Uploaded Image")

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

        # Load custom YOLO model named "best.pt"
        model = YOLO('best.pt')  # Adjust the path if necessary

        # Make predictions using the uploaded image
        results = model(img_array, imgsz=640)

        # Render the images with bounding boxes
        rendered_imgs = results.render()
        
        if rendered_imgs:
            display_img = rendered_imgs[0]
            st.image(display_img, use_column_width=True, caption="YOLO Predictions")

         # For displaying crops
         # This logic assumes `results.pred[0]` contains bounding box coordinates.
            for i, (x1, y1, x2, y2, conf, class_num) in enumerate(results.pred[0]):
                crop = img_array[int(y1):int(y2), int(x1):int(x2)]
                st.image(crop, use_column_width=False, caption=f"Object {i+1}")

if __name__ == "__main__":
    main()
