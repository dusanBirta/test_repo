# Import required libraries

import streamlit as st
import PIL

# Setting page layout
st.set_page_config(
    page_title="Object Detection using YOLOv8",  # Setting page title
    page_icon="🤖",     # Setting page icon
    layout="wide",      # Setting layout to wide
    initial_sidebar_state="expanded"    # Expanding sidebar by default
)

# Creating sidebar
with st.sidebar:
    st.header("Image/Video Config")     # Adding header to sidebar
    # Adding file uploader to sidebar for selecting images
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

# Creating main page heading
st.title("Object Detection using YOLOv8")

# Creating two columns on the main page
col1, col2 = st.columns(2)

# Adding image to the first column if image is uploaded
with col1:
    if source_img:
        # Opening the uploaded image
        uploaded_image = PIL.Image.open(source_img)
        # Adding the uploaded image to the page with a caption
        st.image(source_img,
                 caption="Uploaded Image",
                 use_column_width=True
                 )
