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
    st.title("Image Classification")

    # Open webcam
    cap = cv2.VideoCapture(0)

    # Loop for capturing frames and performing prediction
    start_time = time.time()
    while True:
        ret, frame = cap.read()

        # Display the frame
        st.image(frame, channels="BGR", use_column_width=True)

        # Perform prediction after 3 seconds
        if time.time() - start_time >= 3:
            # Predict gesture
            gesture = predict_gesture(frame)

            # Display the predicted gesture
            if gesture == 0:
                st.write("You made a Rock!")
            elif gesture == 1:
                st.write("You made a Paper!")
            elif gesture == 2:
                st.write("You made Scissors!")
            break

    # Release the webcam
    cap.release()

if __name__ == '__main__':
    main()
