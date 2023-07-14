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
    st.title("Rock Paper Scissors Image Classification")

    # Button to start webcam
    start_button = st.button("Start Webcam")

    # Initialize variables
    img_file_buffer = None
    cv2_img = None

    if start_button:
        # Capture image from webcam
        img_file_buffer = st.camera_input("Take a picture")

    if img_file_buffer is not None:
        # Read image file buffer with OpenCV
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        # Display the captured image
        st.image(cv2_img, channels="BGR", use_column_width=True)

        # Predict gesture
        gesture = predict_gesture(cv2_img)

        # Display the predicted gesture
        if gesture == 0:
            st.write("You made a Rock!")
        elif gesture == 1:
            st.write("You made a Paper!")
        elif gesture == 2:
            st.write("You made Scissors!")

if __name__ == '__main__':
    main()
