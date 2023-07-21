import streamlit as st
import cv2
import numpy as np

# Function to get the middle section of the image
def get_middle_section(image):
    height, width, _ = image.shape
    middle_x, middle_y = int(width / 2), int(height / 2)
    return image[middle_y - 50 : middle_y + 50, middle_x - 50 : middle_x + 50]

def main():
    st.title("Mouse Writing App")

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image using OpenCV
        image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image, 1)

        # Get the middle section of the image
        middle_section = get_middle_section(image)

        # Display the original image
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Show the middle section of the image
        st.image(middle_section, caption="Middle Section", use_column_width=True)

        # Convert the image to RGB (OpenCV uses BGR by default)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Function to handle mouse events
        def mouse_event(event, x, y, flags, param):
            if event == cv2.EVENT_MOUSEMOVE:
                # Check if the mouse is hovering over the middle section
                middle_x, middle_y = int(image.shape[1] / 2), int(image.shape[0] / 2)
                if middle_x - 50 <= x <= middle_x + 50 and middle_y - 50 <= y <= middle_y + 50:
                    # Write "Mouse is hovering" on the image
                    cv2.putText(image_rgb, "Mouse is hovering", (middle_x - 50, middle_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        # Create a window to display the image
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", mouse_event)

        while True:
            # Display the image with OpenCV
            cv2.imshow("Image", image_rgb)

            # Exit the loop if the user presses the 'Esc' key
            if cv2.waitKey(1) == 27:
                break

        # Close the OpenCV window
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
