import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image

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

    # Capture image from webcam
    picture = st.camera_input("Take a picture")

    # Perform prediction if an image is captured
    if picture is not None:
        # Convert the captured image to NumPy array
        image_array = np.array(picture)

        # Convert NumPy array to PIL Image
        pil_image = Image.fromarray(np.uint8(image_array))

        # Convert PIL Image to OpenCV format
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Display the captured image
        st.image(cv_image, channels="BGR", use_column_width=True)

        # Predict gesture
        gesture = predict_gesture(cv_image)

        # Display the predicted gesture
        if gesture == 0:
            st.write("You made a Rock!")
        elif gesture == 1:
            st.write("You made a Paper!")
        elif gesture == 2:
            st.write("You made Scissors!")

if __name__ == '__main__':
    main()
