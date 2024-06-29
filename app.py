from ultralytics import YOLO
from PIL import Image
import streamlit as st
from pathlib import Path
import PIL
from model import run_batch

# Setting page layout
st.set_page_config(
    page_title="Heineken",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Heineken")

# Sidebar
st.sidebar.header("Settings")

st.sidebar.header("Task Config")
task = st.sidebar.radio(
    "Select Task", ['Branding detection', 'PG Monitoring', 'Promotion Kit'])

uploaded_files = st.sidebar.file_uploader(
    "Upload Image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)
# Main content
if uploaded_files:
    st.subheader("Uploaded Images")
    images = []
    for uploaded_file in uploaded_files:
        image = PIL.Image.open(uploaded_file)
        images.append(image)
        st.image(image, caption=uploaded_file.name, use_column_width=True)
    
    results = run_batch(images)
    st.subheader("Results")
    for i, result in enumerate(results):
        # Display the processed image
        st.image(f'result/image_{i}.jpg', caption=f'Processed Image {i}', use_column_width=False)
        
        # Display the bounding box details
        if result.boxes is not None:
            st.write(f"Image {i} - Bounding Boxes:")
            for box in result.boxes:
                st.write(f"Box: {box.xyxy}, Confidence: {box.conf}, Class: {box.cls}")

        # Display other details if available
        if result.masks is not None:
            st.write(f"Image {i} - Masks:")
            st.write(result.masks)

        if result.keypoints is not None:
            st.write(f"Image {i} - Keypoints:")
            st.write(result.keypoints)

        if result.probs is not None:
            st.write(f"Image {i} - Probabilities:")
            st.write(result.probs)

        if result.obb is not None:
            st.write(f"Image {i} - Oriented Bounding Boxes:")
            st.write(result.obb)

else:
    st.info("Please upload one or more images to proceed.")
