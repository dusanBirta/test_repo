import streamlit as st
import base64

def main():
    st.title("Mouse Hover App")

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, use_column_width=True, caption="Uploaded Image")

        # Read the image as bytes and convert it to base64
        if uploaded_file.type.startswith("image/"):
            img_bytes = uploaded_file.read()
            img_base64 = base64.b64encode(img_bytes).decode()

            # Custom HTML template for the tooltip
            tooltip_html = f"""
            <div style="position: relative; display: inline-block;">
                <img src="data:image/png;base64,{img_base64}" alt="Image" width="400" height="400"
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
