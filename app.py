import streamlit as st
import base64

def main():
    st.title("Mouse Click App")

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, use_column_width=True, caption="Uploaded Image")

        # Read the image as bytes and convert it to base64
        if uploaded_file.type.startswith("image/"):
            img_bytes = uploaded_file.read()
            img_base64 = base64.b64encode(img_bytes).decode()

            # Custom HTML template for the click event
            click_html = f"""
            <div style="position: relative; display: inline-block;">
                <img src="data:image/png;base64,{img_base64}" alt="Image" width="400" height="400"
                     onclick="handleClick(event)">
                <div id="message" style="visibility: hidden; width: 100px; background-color: #555; color: #fff;
                            text-align: center; border-radius: 6px; padding: 5px; position: absolute;
                            z-index: 1;">
                    Click
                </div>
            </div>
            <script>
                function handleClick(event) {{
                    var message = document.getElementById('message');
                    var mouseX = event.clientX;
                    var mouseY = event.clientY;
                    message.style.left = mouseX + 'px';
                    message.style.top = mouseY + 'px';
                    message.style.visibility = 'visible';
                }}
            </script>
            """

            # Display the image with the click event
            st.components.v1.html(click_html, height=400, scrolling=False)

if __name__ == "__main__":
    main()
