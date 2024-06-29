from ultralytics import YOLO
from PIL import Image
import streamlit as st
from pathlib import Path
import PIL
from model import run_batch, display
from result_class import resultClassList, getClassName
from utils import model
from itertools import compress

name = model.names
results = None
ok = True


pre_uploaded_files = None 
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
st.sidebar.header("TASK MENU")

#st.sidebar.header("Task Config")
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
    
    # Check if uploaded files have changed to trigger new processing
    if "pre_uploaded_files" not in st.session_state or st.session_state.pre_uploaded_files != uploaded_files:
        results = run_batch(images)
        st.session_state.images = images
        display(st.session_state.images, results, resultClassList(results))
        st.session_state.pre_uploaded_files = uploaded_files
        st.session_state.results = results

    # Sidebar for task-specific configurations
    with st.sidebar:
        if st.session_state.results is not None:
            st.session_state.class_list = resultClassList(st.session_state.results)
            st.session_state.class_checklist = [st.checkbox(getClassName(id), value=True, key=f"{i}") for i, id in enumerate(st.session_state.class_list)]

    st.subheader("Results")
    for i, result in enumerate(st.session_state.results):
        # Display the processed image
        # print(images)
        display(st.session_state.images, st.session_state.results, list(compress(st.session_state.class_list,st.session_state.class_checklist)))
        st.image(f'result/image_{i}.jpg', caption=f'Processed Image {i}', use_column_width=False)
else:
    st.info("Please upload one or more images to proceed.")
