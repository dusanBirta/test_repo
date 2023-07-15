import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import urllib

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

# Function to get randomly selected gesture image
def get_random_gesture_image():
    gesture_images = ["rock.jpg", "paper.jpg", "scissors.jpg"]  # Replace with actual file names
    random_image = np.random.choice(gesture_images)
    return random_image

# Streamlit app
def main():
    # Set page title
    st.title("Rock, Paper, Scissors, Game")

    # Picture Taken
    picture = st.camera_input("Take a picture")

    # Perform prediction if an image is uploaded
    if picture:
        # Read the uploaded file
        file_bytes = np.asarray(bytearray(picture.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Display the uploaded image
        st.image(image, channels="BGR", use_column_width=True)

        # Predict gesture
        gesture = predict_gesture(image)

        # Display the predicted gesture
        if gesture == 0:
            st.write("You made Rock!")
        elif gesture == 1:
            st.write("You made Paper!")
        elif gesture == 2:
            st.write("You made Scissors!")

        # Get randomly selected gesture image
        gesture_image_file = get_random_gesture_image()
        gesture_image = cv2.imread(gesture_image_file)

        if gesture_image_file == "rock.jpg":
            st.write("Computer made Rock!")
            computer_gesture = 0
        elif gesture_image_file == "paper.jpg":
            st.write("Computer made Paper!")
            computer_gesture = 1
        elif gesture_image_file == "scissors.jpg":
            st.write("Computer made Scissors!")
            computer_gesture = 2

        # Display the generated rock, paper, or scissors image
        st.image(gesture_image, channels="BGR", use_column_width=True)

        # Compare the gestures and declare the winner
        if gesture == computer_gesture:
            st.write("It's a tie!")
        elif (gesture == 0 and computer_gesture == 2) or (gesture == 1 and computer_gesture == 0) or (gesture == 2 and computer_gesture == 1):
            st.write("You win!")
        else:
            st.write("Computer wins!")

if __name__ == '__main__':
    main()
