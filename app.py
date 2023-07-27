from ultralytics import YOLO
import streamlit as st
import base64
from PIL import Image
import io
import cv2
import numpy as np


def main():
    st.title("YOLOv8 Predictions with Mouse Click App")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        img_width, img_height = image.size

        model = YOLO('best.pt')  
        results = model(img_array)
        result = results[0]

        boxes = result.boxes  
        box_areas = []  # list to store bounding box coordinates for the JavaScript

        label_font_scale = 0.75
        box_thickness = 3
        readable_colors = [(80, 80, 80), (80, 255, 80), (80, 80, 255), (255, 255, 80), (80, 255, 255)]

        for (x1, y1, x2, y2, conf, class_num) in boxes.data:
            box_areas.append([x1, y1, x2, y2])
            label = result.names[int(class_num)]
            color = readable_colors[int(class_num) % len(readable_colors)]
            cv2.rectangle(img_array, (int(x1), int(y1)), (int(x2), int(y2)), color, box_thickness)
            cv2.putText(img_array, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, label_font_scale, color, 2)

        is_success, img_buffer = cv2.imencode(".png", img_array)
        if is_success:
            img_bytes = img_buffer.tobytes()

        click_html = f"""
        <div style="position: relative; display: inline-block;">
            <img src="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" alt="Image" width="{img_width}" height="{img_height}" onclick="handleClick(event)" onmousemove="handleMouseOver(event)">
        </div>
        <script>
            var descriptions = {{}};
            var boxAreas = {box_areas};

            function handleClick(event) {{
                var mouseX = event.offsetX;
                var mouseY = event.offsetY;

                for (var i = 0; i < boxAreas.length; i++) {{
                    var box = boxAreas[i];
                    if (mouseX >= box[0] && mouseX <= box[2] && mouseY >= box[1] && mouseY <= box[3]) {{
                        var description = prompt("Enter a description for this area:");
                        if (description) {{
                            descriptions[mouseX + '-' + mouseY] = description;
                        }}
                        break;
                    }}
                }}
            }}

            function handleMouseOver(event) {{
                var mouseX = event.offsetX;
                var mouseY = event.offsetY;

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
        st.components.v1.html(click_html, height=img_height, width=img_width, scrolling=False)


if __name__ == "__main__":
    main()
