from ultralytics import YOLO
import streamlit as st
from PIL import Image
import cv2
import numpy as np
import base64

def get_clickable_image_html(img_array, boxes):
    # Convert the numpy array image to base64
    is_success, img_buffer = cv2.imencode(".png", img_array)
    img_bytes = img_buffer.tobytes()
    img_base64 = base64.b64encode(img_bytes).decode()

    clickable_img_html = f"""
        <img src="data:image/png;base64,{img_base64}" id="img-upload" style="max-width: 800px;">
        <script>
            var img = document.getElementById('img-upload');
            img.onclick = function(event) {{
                var rect = img.getBoundingClientRect();
                var x = event.clientX - rect.left;
                var y = event.clientY - rect.top;

                // Iterate over bounding boxes to see if the click is inside any
                {boxes}.forEach(box => {{
                    if (x >= box.x1 && x <= box.x2 && y >= box.y1 && y <= box.y2) {{
                        var description = prompt("Enter a description:");
                        // You can save this description and associate it with the box
                    }}
                }});
            }};
        </script>
    """
    return clickable_img_html

def main():
    st.title("YOLOv8 Predictions with Mouse Click App")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image)

        model = YOLO('best.pt')
        results = model(img_array)
        result = results[0]
        boxes = result.boxes

        bounding_boxes_js = []
        for (x1, y1, x2, y2, conf, class_num) in boxes.data:
            label = result.names[int(class_num)]
            color = [128, 128, 128]
            cv2.rectangle(img_array, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)
            cv2.putText(img_array, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            bounding_boxes_js.append({
                'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'label': label
            })

        st.write(get_clickable_image_html(img_array, bounding_boxes_js), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
