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

# Function to get image file based on gesture
def get_gesture_image_file(gesture):
    if gesture == 0:
        return "rock.jpg"  # Replace with actual file name for rock image
    elif gesture == 1:
        return "paper.jpg"  # Replace with actual file name for paper image
    elif gesture == 2:
        return "scissors.jpg"  # Replace with actual file name for scissors image

# Streamlit app
def main():
    # Set page title
    st.title("Rock, Paper, Scissors. Image Classification")

    # Picture Taken
    picture = st.camera_input("Take a picture")

    # Perform prediction if an image is uploaded
    if picture:
        # Read the uploaded file
        file_bytes = np.asarray(bytearray(picture.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Predict gesture
        gesture = predict_gesture(image)

        # Get corresponding gesture image file
        gesture_image_file = get_gesture_image_file(gesture)

        # Display the gesture image
        gesture_image = cv2.imread(gesture_image_file)
        st.image(gesture_image, channels="BGR", use_column_width=True)

        # Compare the gestures and declare the winner
        computer_gesture = np.random.randint(0, 3)
        if gesture == computer_gesture:
            st.write("It's a tie!")
        elif (gesture == 0 and computer_gesture == 2) or (gesture == 1 and computer_gesture == 0) or (gesture == 2 and computer_gesture == 1):
            st.write("You win!")
        else:
            st.write("Computer wins!")

if __name__ == '__main__':
    main()
