// mouse_events.js
const imageElement = document.getElementById("uploaded-image");

// Function to handle click event
imageElement.onclick = (event) => {
  Streamlit.setComponentValue("click");
};

// Function to handle hover event
imageElement.onmousemove = (event) => {
  const rect = imageElement.getBoundingClientRect();
  const mouseX = event.clientX - rect.left;
  const mouseY = event.clientY - rect.top;
  Streamlit.setComponentValue(`hovering at (${mouseX}, ${mouseY})`);
};
