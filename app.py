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
                     onclick="handleClick(event)">
            </div>
            <script>
                // Dictionary to store descriptions and coordinates
                var descriptions = {{}};

                function handleClick(event) {{
                    var mouseX = event.clientX;
                    var mouseY = event.clientY;
                    var description = prompt("Enter a description for this area:");
                    if (description) {{
                        descriptions[description] = {{ x: mouseX, y: mouseY }};
                        updateDescriptions();
                    }}
                }}

                function updateDescriptions() {{
                    var messageDiv = document.getElementById('message');
                    var canvas = document.getElementById('canvas');
                    var ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    // Draw bounding boxes and display descriptions
                    for (var key in descriptions) {{
                        var coord = descriptions[key];
                        ctx.beginPath();
                        ctx.rect(coord.x, coord.y, 100, 50);
                        ctx.lineWidth = 2;
                        ctx.strokeStyle = 'red';
                        ctx.stroke();

                        messageDiv.innerHTML += '<p style="position: absolute; left: ' + coord.x + 'px; top: ' + coord.y + 'px; background-color: #555; color: #fff; border-radius: 6px; padding: 5px;">' + key + '</p>';
                    }}
                }}
            </script>
            <canvas id="canvas" width="400" height="400" style="position: absolute; top: 0; left: 0; pointer-events: none;"></canvas>
            <div id="message" style="position: absolute; top: 0; left: 0;"></div>
            """

            # Display the custom HTML template for the click event
            st.components.v1.html(click_html, height=400, scrolling=False)

if __name__ == "__main__":
    main()
