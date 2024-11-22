import streamlit as st
from solver import puzzle_solver
import os
import time
from main import Camera
import streamlit as st
from camera_input_live import camera_input_live
import cv2
import numpy as np



    



# Title of the app
st.title("OWI Puzzle Solver")

# Instructions for the user
st.write("""
    This app lets you input a Python list, and it will process the list.
    You can input a list of numbers, strings, or any other data type.
""")

# Initialize session state variables
if 'project_name' not in st.session_state:
    st.session_state.project_name = None
    st.session_state.solved_puzzle = None
    st.session_state.played = False
    st.session_state.puzzle=None
    st.session_state.page=1


if st.session_state.page==1:
    title = st.text_input("Movie title", "p1")
    if st.button("Next"):
        if len(title) > 1:
            st.session_state.project_name = title
            st.session_state.page=2
            st.rerun()  # Trigger a rerun to load the next page

if  st.session_state.page==2:
    if 'camera' not in st.session_state:
        st.session_state.camera = Camera()
        st.session_state.puzzle=[]
        st.session_state.pos=[0,0,0,0]
        st.session_state.images=[]
        st.session_state.wait=False
    image = camera_input_live()
    col1,col2=st.columns(2)
    if image:
        bytes_data = image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        rotated_frame, masked_frame, edges, pos=st.session_state.camera.get_frame(cv2_img)
        col1.image(rotated_frame)
        col2.image(edges)
        if sum([1 for i in pos if i==0])<3:
            st.session_state.pos=pos
        st.write(st.session_state.pos)
        col=st.columns(6)
        col[3].write(str(len(st.session_state.images))+'/9')
        if len(st.session_state.images)==9:
            if col[-1].button('Solve Puzzle'):
                st.session_state.page=3
        else:
            col[-1].write(f'{9-len(st.session_state.images)} to Unlock')

        if col[0].button('Scan Next'):
            if False:#sum([1 for i in st.session_state.pos if i==0])>=3:
                st.write('not allowed')
            else:
                st.session_state.images.append(edges)
                st.session_state.puzzle.append(st.session_state.pos)
                st.session_state.wait=True
                st.session_state.pos=[0,0,0,0]

        if st.button('del_last'):
            if len(st.session_state.images)==1:
                st.session_state.images=[]
                st.session_state.puzzle=[]
            if len(st.session_state.images)>2:
                st.session_state.images=st.session_state.images[:-1]
                st.session_state.puzzle=st.session_state.puzzle[:-1]
            if len(st.session_state.images)==2:
                st.session_state.images=st.session_state.images[:1]
                st.session_state.puzzle=st.session_state.puzzle[:1]

        if len(st.session_state.images)>0:
            for count,i in enumerate(st.session_state.images):
                st.write("piece",count+1)
                string='['
                for j in st.session_state.puzzle[count]:
                    string+=str(j)+', '
                string+=']'
                st.write(string)
                st.image(i)
        
        

# Page 2: Puzzle list input (after Next is pressed)
if st.session_state.page==3:
    st.title(st.session_state.project_name)
    cols = st.columns(3)
    if len(st.session_state.images)==9:
    # Loop through the images and assign them to each column in the grid
        for i in range(9):
            with cols[i % 3]:  # Using modulo to cycle through columns
                st.image(st.session_state.images[i], width=150)
    # Input for a Python list
    input_list = st.text_area("Enter a Puzzle List", st.session_state.puzzle)

    # Convert input string to an actual Python list
    try:
        user_list = eval(input_list)
        if not isinstance(user_list, list):
            raise ValueError("Input must be a valid list.")
    except (SyntaxError, ValueError) as e:
        st.error(f"Error: {e}")
        user_list = []

    # Processing the list if it's valid
    if st.button("Next"):
        st.session_state.solved_puzzle,_= puzzle_solver(user_list,st.session_state.project_name)
        st.session_state.page=4
        st.rerun()

if  st.session_state.page==4 :
    st.title('Puzzle Solved')

    # Create a placeholder for the images
    image_placeholder = st.empty()

    # Get list of images from the folder with the same name as project_name
    folder_path = f"./{st.session_state.project_name}"
    if os.path.exists(folder_path):
        image_files = [f for f in os.listdir(folder_path) if f.endswith(('jpg', 'jpeg', 'png'))]
        image_files.sort()  # Sort the images to display in order

        # Display images one by one with a delay of 0.5 seconds
        for img in image_files:
            img_path = os.path.join(folder_path, img)
            # Use the placeholder to update the image dynamically
            image_placeholder.image(img_path,width=500)
            time.sleep(0.5)  # Add a 0.5-second delay between images
    
    else:
        st.error("No images found in the project folder.")
    col=st.columns(3)
    for count,i in enumerate(st.session_state.solved_puzzle):
        col[count//3].write(i[1]+1)
        col[count//3].image(st.session_state.images[i[1]],width=200)

    if st.button('Replay'):
        for img in image_files:
            img_path = os.path.join(folder_path, img)
            # Use the placeholder to update the image dynamically
            image_placeholder.image(img_path, use_column_width=True)
            time.sleep(0.5)  # Add a 0.5-second delay between images
