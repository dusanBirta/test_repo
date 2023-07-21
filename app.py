import streamlit as st
from streamlit.components.v1 import declare_component
import base64

# Declare the custom component with the JavaScript code
mouse_events_component = declare_component(
    "mouse_events",
    url="mouse_events.js",
)

def main():
    st.title("Mouse Events App")

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, use_column_width=True, caption="Uploaded Image")

        # Read the image as bytes and convert it to base64
        if uploaded_file.type.startswith("image/"):
            img_bytes = uploaded_file.read()
            img_base64 = base64.b64encode(img_bytes).decode()

            # Pass the base64 string to the custom component
            result = mouse_events_component(uploaded_image=img_base64)

            # Display the dynamic updates based on mouse events
            if result is not None:
                if "click" in result:
                    st.image(img_bytes, use_column_width=True, caption="Click: 'click'")

                if "hovering" in result:
                    st.image(img_bytes, use_column_width=True, caption=f"Hover: {result}")

if __name__ == "__main__":
    main()
