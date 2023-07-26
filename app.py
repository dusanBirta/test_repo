from ultralytics import YOLO
import streamlit as st
import base64
from PIL import Image
from io import BytesIO

# Import the YOLOv8 model
#from yolov8 import YOLO

def predict_with_yolov8(img_bytes):
    # Load YOLOv8 model with the weights file "best.pt"
    model = YOLO(weights="best.pt")

    # Convert the image bytes to PIL image
    pil_image = Image.open(BytesIO(img_bytes))

    # Run inference on the image
    results = model(pil_image)

    return results

def main():
    st.title("YOLOv8 Predictions with Mouse Click App")

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image as bytes
        img_bytes = uploaded_file.read()

        # Display the uploaded image
        st.image(img_bytes, use_column_width=True, caption="Uploaded Image")

        # Predict with YOLOv8
        results = predict_with_yolov8(img_bytes)

        # Display YOLOv8 predictions
        if len(results.imgs) > 0:
            st.image(results.imgs[0], use_column_width=True, caption="YOLOv8 Predictions")

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

if __name__ == "__main__":
    main()
