import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import av
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# Load pre-trained model
model = load_model('rock_paper_scissors_cnn.h5')

# Function to preprocess the image
def preprocess_image(image):
    img = cv2.resize(image, (128, 128))
    img = tf.cast(img, tf.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# Function to predict the gesture
def predict_gesture(frame):
    image = frame.to_ndarray(format="bgr24")
    preprocessed_image = preprocess_image(image)
    prediction = model.predict(preprocessed_image)
    predicted_class = np.argmax(prediction)
    return predicted_class

# Streamlit app
def main():
    # Set page title
    st.title("Image Classification")

    # Perform prediction using webcam
    class VideoProcessor:
        def __init__(self):
            self.frame = None

        def recv(self, frame):
            self.frame = frame
            return av.VideoFrame.from_ndarray(frame.to_ndarray(format="bgr24"), format="bgr24")

    video_processor = VideoProcessor()
    webrtc_streamer(
        key="WYH",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        ),
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=video_processor,
        async_processing=True,
    )

    # Predict gesture
    if video_processor.frame is not None:
        gesture = predict_gesture(video_processor.frame)

        # Display the predicted gesture
        if gesture == 0:
            st.write("You made a Rock!")
        elif gesture == 1:
            st.write("You made a Paper!")
        elif gesture == 2:
            st.write("You made Scissors!")

if __name__ == '__main__':
    main()
