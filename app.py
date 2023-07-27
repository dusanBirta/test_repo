from ultralytics import YOLO
import streamlit as st
import base64
from PIL import Image
import cv2
import numpy as np

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

        box_areas = []
        for (x1, y1, x2, y2, conf, class_num) in boxes.data:
            label = result.names[int(class_num)]
            color = [128, 128, 128]
            cv2.rectangle(img_array, (int(x1), int(y1)), (int(x2), int(y2)), color, 3)
            cv2.putText(img_array, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            box_areas.append([x1, y1, x2, y2])

        is_success, img_buffer = cv2.imencode(".png", img_array)
        if is_success:
            img_bytes = img_buffer.tobytes()

        box_areas_str = str(box_areas).replace(" ", "")

        click_html = f"""
        <div style="position: relative; display: inline-block;">
            <img src="data:image/png;base64,{base64.b64encode(img_bytes).decode()}" alt="Image" style="max-width: 800px;" onclick="handleClick(event)">
        </div>
        <script>
            var boxAreas = {box_areas_str};

            function handleClick(event) {{
                var mouseX = event.offsetX;
                var mouseY = event.offsetY;

                for (var i = 0; i < boxAreas.length; i++) {{
                    var box = boxAreas[i];
                    if (mouseX >= box[0] && mouseX <= box[2] && mouseY >= box[1] && mouseY <= box[3]) {{
                        var description = prompt("Enter a description for this area:");
                        if (description) {{
                            window.location.href = '/?description=' + description;
                        }}
                        break;
                    }}
                }}
            }}
        </script>
        """

        st.components.v1.html(click_html, height=720, scrolling=False)

        description = st.experimental_get_query_params().get('description')
        if description:
            st.write(f"Description added: {description[0]}")

if __name__ == "__main__":
    main()
