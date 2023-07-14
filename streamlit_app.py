import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load pre-trained model
model = load_model('rock_paper_scissors_cnn.h5')

# Function to preprocess the image
def preprocess_image(image):
    img = cv2.resize(image, (128, 128))
    img = tf.cast(img, tf.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Function to predict the gesture
def predict_gesture(image):
    preprocessed_image = preprocess_image(image)
    prediction = model.predict(preprocessed_image)
    predicted_class = np.argmax(prediction)
    return predicted_class

# Streamlit app
def main():
    # Set page title
    st.title("Image Classification")

    # File uploader
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Perform prediction if an image is uploaded
    if uploaded_file is not None:
        # Read the uploaded file
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Display the uploaded image
        st.image(image, channels="BGR", use_column_width=True)

        # Predict gesture
        gesture = predict_gesture(image)

        # Display the predicted gesture
        if gesture == 0:
            st.write("You made a Rock!")
        elif gesture == 1:
            st.write("You made a Paper!")
        elif gesture == 2:
            st.write("You made Scissors!")

if __name__ == '__main__':
    main()
