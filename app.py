import streamlit as st
from solver import puzzle_solver
import os
import time

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
    st.session_state.input_puzzle = []
    st.session_state.solved_puzzle = None
    st.session_state.played = False

# Page 1: Movie title input
if st.session_state.project_name is None and len(st.session_state.input_puzzle)<1:
    title = st.text_input("Movie title", "p1")
    if st.button("Next"):
        if len(title) > 1:
            st.session_state.project_name = title
            st.rerun()  # Trigger a rerun to load the next page

# Page 2: Puzzle list input (after Next is pressed)
if st.session_state.project_name is not None and st.session_state.solved_puzzle is None:
    st.title(st.session_state.project_name)

    # Input for a Python list
    input_list = st.text_area("Enter a Puzzle List", "['1', '2', '3', '4']")

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
        st.rerun()

if  st.session_state.solved_puzzle is not None and  not st.session_state.played :
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
            image_placeholder.image(img_path, use_column_width=True)
            time.sleep(0.5)  # Add a 0.5-second delay between images

    else:
        st.error("No images found in the project folder.")
    
    if st.button('Replay'):
        for img in image_files:
            img_path = os.path.join(folder_path, img)
            # Use the placeholder to update the image dynamically
            image_placeholder.image(img_path, use_column_width=True)
            time.sleep(0.5)  # Add a 0.5-second delay between images
