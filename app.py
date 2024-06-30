from PIL import Image, ImageDraw, ImageFont
import streamlit as st
import PIL
from model import run_batch, display  # Importing functions from your model
from itertools import compress
from result_class import resultClassList, getClassName  # Utility functions
from utils import is_inside_soft  # Utility function for containment check

# Initialize translated dictionary
translated = {
    'beer_keg': 'Beer Keg',
    'tiger_logo': 'Tiger Logo',
    'larue_logo': 'LaRue Logo',
    'heineken_logo': 'Heineken Logo',
    'biaviet_logo': 'Biaviet Logo',
    'beer_bottle': 'Beer Bottle',
    'consumer': 'Consumer',
    'bivina_logo': 'Bivina Logo',
    'staff': 'Staff',
    'saigon_logo': 'Saigon Logo',
    'billboard': 'Billboard',
    'signage': 'Signage',
    'bucket': 'Bucket',
    'campain-objects': 'Campaign Objects',
    'pg_marketer': 'PG Marketer',
    'fridge': 'Fridge',
    'strongbow_logo': 'Strongbow Logo',
    'standee': 'Standee',
    'tent-card': 'Tent Card',
    'parasol': 'Parasol',
    'display-stand': 'Display Stand'
}


# Setting page layout
st.set_page_config(
    page_title="Heineken Brand Detection",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Heineken Brand Detection")

# Sidebar
st.sidebar.header("TASK MENU")
task = st.sidebar.radio("Select Task", ['Branding detection', 'PG Monitoring', 'Promotion Kit'])

# File uploader for images
uploaded_files = st.sidebar.file_uploader(
    "Upload Image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)
if task == 'Branding detection':
    # Main content
    if uploaded_files:
        st.subheader("Uploaded Images")
        images = []
        for uploaded_file in uploaded_files:
            image = PIL.Image.open(uploaded_file)
            images.append(image)
        
        # Display uploaded images in a grid
        col1, col2 = st.columns(2)
        for i, image in enumerate(images):
            with col1:
                st.image(image, caption=uploaded_files[i].name, use_column_width=True)
                
        # Check if uploaded files have changed to trigger new processing
        if "pre_uploaded_files" not in st.session_state or st.session_state.pre_uploaded_files != uploaded_files:
            results = run_batch(images)  # Process images using your model
            st.session_state.images = images
            st.session_state.results = results
            st.session_state.pre_uploaded_files = uploaded_files
            st.session_state.image_paths = [f'image_{i}.jpg' for i in range(len(results))]  # Placeholder for image paths
            
        # Display checkboxes for logo types in sidebar
        if st.session_state.results:
            with st.sidebar:
                st.session_state.class_list = resultClassList(st.session_state.results)
                st.session_state.class_checklist = [st.checkbox(getClassName(id), value=True, key=f"{i}") for i, id in enumerate(st.session_state.class_list)]
                st.subheader("Choose Logo Type")
                selected_type = st.radio("Select Logo Type", list(filter(lambda class_name: class_name.endswith('_logo'), map(getClassName, st.session_state.class_list))), index=0, key=f"radio_logo")
                st.session_state.selected_logo_type = selected_type
            
            # Display processed images with highlighted logos and contained objects
            for i, result in enumerate(st.session_state.results):
                processed_image = st.session_state.images[i].copy()
                draw = ImageDraw.Draw(processed_image)
                bboxes = result.boxes.xyxy
                cls_ids = result.boxes.cls
                
                for j, (bbox, cls_id) in enumerate(zip(bboxes, cls_ids)):
                    if getClassName(int(cls_id)) == st.session_state.selected_logo_type:
                        logo_bbox = bbox
                        logo_label = getClassName(int(cls_id))
                        draw.rectangle([(logo_bbox[0], logo_bbox[1]), (logo_bbox[2], logo_bbox[3])], outline="blue", width=3)

                        # Check containment of other bounding boxes within this logo
                        for k, (bbox_, cls_id_) in enumerate(zip(bboxes, cls_ids)):
                            if j != k and is_inside_soft(logo_bbox, bbox_):
                                contained_label = getClassName(int(cls_id_))
                                img_fraction = 0.50
                                fontsize = 20
                                font = ImageFont.truetype("arial.ttf", fontsize)
                                draw.rectangle([(bbox_[0], bbox_[1]), (bbox_[2], bbox_[3])], outline="red", width=5)
                                draw.text((bbox_[0] + 5, bbox_[1] + 5), f'{translated[contained_label]}', fill='white', stroke_fill='black', font=font)
                                break
                
                with col2:
                    st.image(processed_image, caption=f'Processed Image {i+1}', use_column_width=True)
    else:
        st.info("Please upload one or more images to proceed.")

elif task == 'PG Monitoring':
    # Main content
    if uploaded_files:
        st.subheader("Uploaded Images")
        images = []
        for uploaded_file in uploaded_files:
            image = PIL.Image.open(uploaded_file)
            images.append(image)
        
        # Display uploaded images in a grid
        col1, col2 = st.columns(2)
        for i, image in enumerate(images):
            with col1:
                st.image(image, caption=uploaded_files[i].name, use_column_width=True)
                st.subheader("")
                
        # Check if uploaded files have changed to trigger new processing
        if "pre_uploaded_files" not in st.session_state or st.session_state.pre_uploaded_files != uploaded_files:
            results = run_batch(images)  # Process images using your model
            st.session_state.images = images
            st.session_state.results = results
            st.session_state.pre_uploaded_files = uploaded_files
            st.session_state.image_paths = [f'image_{i}.jpg' for i in range(len(results))]  # Placeholder for image paths

        if st.session_state.results:
            with st.sidebar:
                st.session_state.class_list = resultClassList(st.session_state.results)
                st.session_state.class_checklist = [st.checkbox(getClassName(id), value=True, key=f"{i}") for i, id in enumerate(st.session_state.class_list)]
                
        
             
            
            for i, result in enumerate(st.session_state.results):
                total_pg_marketers = 0
                processed_image = st.session_state.images[i].copy()
                draw = ImageDraw.Draw(processed_image)
                bboxes = result.boxes.xyxy
                cls_ids = result.boxes.cls
                for j, (bbox, cls_id) in enumerate(zip(bboxes, cls_ids)):
                    if getClassName(int(cls_id)) == 'pg_marketer':
                        total_pg_marketers += 1
                        logo_label = getClassName(int(cls_id))
                        draw.rectangle([(bbox[0], bbox[1]), (bbox[2], bbox[3])], outline="blue", width=5)
                with col2:
                    st.image(processed_image, caption=f'Processed Image {i+1}', use_column_width=True)
                    st.subheader(f"Total PG Marketers: {total_pg_marketers}")
                    

elif task == 'Promotion Kit':
    # Main content
    if uploaded_files:
        st.subheader("Uploaded Images")
        images = []
        for uploaded_file in uploaded_files:
            image = PIL.Image.open(uploaded_file)
            images.append(image)
        
        # Display uploaded images in a grid
        col1, col2 = st.columns(2)
        for i, image in enumerate(images):
            with col1:
                st.image(image, caption=uploaded_files[i].name, use_column_width=True)
                st.subheader("")
                st.subheader("")
                st.subheader("")
                
        # Check if uploaded files have changed to trigger new processing
        if "pre_uploaded_files" not in st.session_state or st.session_state.pre_uploaded_files != uploaded_files:
            results = run_batch(images)  # Process images using your model
            st.session_state.images = images
            st.session_state.results = results
            st.session_state.pre_uploaded_files = uploaded_files
            st.session_state.image_paths = [f'image_{i}.jpg' for i in range(len(results))]  # Placeholder for image paths

        if st.session_state.results:
            with st.sidebar:
                st.session_state.class_list = resultClassList(st.session_state.results)
                st.session_state.class_checklist = [st.checkbox(getClassName(id), value=True, key=f"{i}") for i, id in enumerate(st.session_state.class_list)]
                st.subheader("Choose Logo Type")
                selected_type = st.radio("Select Logo Type", list(filter(lambda class_name: class_name.endswith('_logo'), map(getClassName, st.session_state.class_list))), index=0, key=f"radio_logo")
                st.session_state.selected_logo_type = selected_type
        
             
            
            for i, result in enumerate(st.session_state.results):
                total_billboard = 0
                total_standee = 0
                total_beer_keg = 0 
                processed_image = st.session_state.images[i].copy()
                draw = ImageDraw.Draw(processed_image)
                bboxes = result.boxes.xyxy
                cls_ids = result.boxes.cls
                used = [False] * len(bboxes)
                for j, (bbox, cls_id) in enumerate(zip(bboxes, cls_ids)):
                    if getClassName(int(cls_id)) == st.session_state.selected_logo_type:
                        logo_bbox = bbox
                        logo_label = getClassName(int(cls_id))
                        draw.rectangle([(logo_bbox[0], logo_bbox[1]), (logo_bbox[2], logo_bbox[3])], outline="blue", width=3)

                        # Check containment of other bounding boxes within this logo
                        for k, (bbox_, cls_id_) in enumerate(zip(bboxes, cls_ids)):
                            if not used[k] and getClassName(int(cls_id_)) in ['billboard', 'signage', 'standee', 'beer_keg'] and j != k and is_inside_soft(logo_bbox, bbox_):
                                contained_label = getClassName(int(cls_id_))
                                img_fraction = 0.50
                                fontsize = 20
                                if getClassName(int(cls_id_)) == 'billboard' or getClassName(int(cls_id_)) == 'signage': 
                                    total_billboard += 1
                                elif getClassName(int(cls_id_)) == 'standee': 
                                    total_standee += 1
                                else: 
                                    total_beer_keg += 1
                                print(getClassName(int(cls_id_)), total_billboard, total_standee, total_beer_keg)
                                font = ImageFont.truetype("arial.ttf", fontsize)
                                draw.rectangle([(bbox_[0], bbox_[1]), (bbox_[2], bbox_[3])], outline="red", width=5)
                                draw.text((bbox_[0] + 5, bbox_[1] + 5), f'{translated[contained_label]}', fill='white', stroke_fill='black', font=font)
                                used[k] = True
                                break
                
                with col2:
                    st.image(processed_image, caption=f'Processed Image {i+1}', use_column_width=True)
                    st.subheader(f"Total Billboard/Signage: {total_billboard}")
                    st.subheader(f"Total Standee: {total_standee}")
                    st.subheader(f"Total Beer Keg: {total_beer_keg}")

        # print total number of pg_marketer