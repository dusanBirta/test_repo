import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import time
import streamlit as st

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
    st.title("WEbCam Image Classification")

    # Capture frames from the webcam
    frame = st.empty()

    # Wait for 3 seconds
    time.sleep(3)

    # Capture a single frame
    frame_data = st.camera_input(width=128, height=128, use_column_width=False)
    if frame_data is not None:
        frame.image(frame_data, channels="BGR", use_column_width=True)

        # Predict gesture
        gesture = predict_gesture(frame_data)

        # Display the predicted gesture
        if gesture == 0:
            st.write("You made a Rock!")
        elif gesture == 1:
            st.write("You made a Paper!")
        elif gesture == 2:
            st.write("You made Scissors!")

if __name__ == '__main__':
    main()
