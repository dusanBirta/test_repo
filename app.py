import streamlit as st
import base64
import torch
from ultralytics import YOLO
from PIL import Image

def predict_with_yolov8(img_bytes):
    # Load YOLOv8 model with the weights file
    model = YOLO("yolov8n.pt", weights="best.pt")

    # Convert the image bytes to PIL image
    pil_image = Image.open(io.BytesIO(img_bytes))

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
        if "pred" in results.names:
            st.image(results.pred[0].get_image(), use_column_width=True, caption="YOLOv5 Predictions")

        # Custom HTML template for the click event
        click_html = f"""
        <div style="position: relative; display: inline-block;">
            <img src="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" alt="Image" width="400" height="400"
                 onclick="handleClick(event)" onmousemove="handleMouseOver(event)">
        </div>
        <script>
            // Your existing handleClick and handleMouseOver functions here

            // ...
        </script>
        <div id="message" style="position: absolute; top: 0; left: 0;"></div>
        """

        # Display the custom HTML template for the click event
        st.components.v1.html(click_html, height=400, scrolling=False)

if __name__ == "__main__":
    main()
