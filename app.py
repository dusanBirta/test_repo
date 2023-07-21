import streamlit as st
import base64

def main():
    st.title("Mouse Click App")

    # File uploader to get the image from the user
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image as bytes and convert it to base64
        if uploaded_file.type.startswith("image/"):
            img_bytes = uploaded_file.read()
            img_base64 = base64.b64encode(img_bytes).decode()

            # Custom HTML template for the click event
            click_html = f"""
            <div style="position: relative; display: inline-block;">
                <img src="data:image/png;base64,{img_base64}" alt="Image" width="400" height="400"
                     onclick="handleClick(event)" onmousemove="handleMouseOver(event)">
            </div>
            <script>
                // Dictionary to store descriptions and coordinates
                var descriptions = {{}};

                function handleClick(event) {{
                    var mouseX = event.clientX;
                    var mouseY = event.clientY;
                    var description = prompt("Enter a description for this area:");
                    if (description) {{
                        descriptions[`${mouseX}-${mouseY}`] = description;
                    }}
                }}

                function handleMouseOver(event) {{
                    var mouseX = event.clientX;
                    var mouseY = event.clientY;

                    var messageDiv = document.getElementById('message');
                    messageDiv.innerHTML = '';

                    // Display descriptions for the hovered area
                    for (var key in descriptions) {{
                        var coords = key.split('-');
                        var distance = Math.sqrt((mouseX - coords[0]) ** 2 + (mouseY - coords[1]) ** 2);
                        if (distance <= 50) {{  // Only display descriptions within a radius of 50 pixels
                            messageDiv.innerHTML += '<p style="position: absolute; left: ' + coords[0] + 'px; top: ' + coords[1] + 'px; background-color: #555; color: #fff; border-radius: 6px; padding: 5px;">' + descriptions[key] + '</p>';
                        }}
                    }}
                }}
            </script>
            <div id="message" style="position: absolute; top: 0; left: 0;"></div>
            """

            # Display the custom HTML template for the click event
            st.components.v1.html(click_html, height=400, scrolling=False)

if __name__ == "__main__":
    main()
