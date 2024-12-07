import streamlit as st
from solver import puzzle_solver
import os
import time
from main import Camera
import streamlit as st
from camera_input_live import camera_input_live
import cv2
import numpy as np
from drawing_tools import display_images
import json
import serial

def load_puzzle(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"File '{filename}' not found!")
        return None

# Input for the filename

st.title("OWI Puzzle Solver")


if 'page' not in st.session_state:
    st.session_state.page=-1


if st.session_state.page==-1:
    # Instructions for the user
    st.image('./display_image.png')
    st.write("""
        This app lets you input a Python list, and it will process the list.
        You can input a list of numbers, strings, or any other data type.
    """)
    if st.button('Start'):
        st.session_state.page=0
        st.rerun()

    filename = st.text_input("Enter the filename to load the puzzle")
    if st.button('Load'):
        if filename:
            st.session_state.project_name=filename
            solved_puzzle = load_puzzle(st.session_state.project_name+'/solved_puzzle.json')
            
            if solved_puzzle:
                st.session_state.solved_puzzle = solved_puzzle
                st.success("Puzzle loaded successfully!")
                st.write(f"Loaded puzzle: {st.session_state.solved_puzzle}")
                time.sleep(1)
                st.session_state.page=6
                st.rerun()
        else:
            st.error("Please provide a filename.")
        
if st.session_state.page==0:
    st.session_state.project_name = None
    st.session_state.solved_puzzle = None
    st.session_state.played = False
    st.session_state.puzzle=None
    st.session_state.page=1


if st.session_state.page==1:
    title = st.text_input("Project title", "p1")
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
    col1,col2,col3=st.columns(3)
    if image:
        bytes_data = image.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        rotated_frame, masked_frame, edges, pos=st.session_state.camera.get_frame(cv2_img)
        col1.image(rotated_frame)
        col2.image(edges)
        if sum([1 for i in pos if i==0])<3:
            st.session_state.pos=pos
        col3.image(display_images(st.session_state.pos))
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
        for i in range(9):
            with cols[i % 3]:  # Using modulo to cycle through columns
                st.image(display_images(st.session_state.puzzle[i]), width=150)
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
    image_placeholder = st.empty()
    print(st.session_state.puzzle)
    folder_path = f"./{st.session_state.project_name}"
    if os.path.exists(folder_path):
        image_files = [f for f in os.listdir(folder_path) if f.endswith(('jpg', 'jpeg', 'png'))]
        image_files.sort()
        for img in image_files:
            img_path = os.path.join(folder_path, img)
            image_placeholder.image(img_path,width=500)
            time.sleep(0.5)
    
    else:
        st.error("No images found in the project folder.")
    col=st.columns(3)
    for count,i in enumerate(st.session_state.solved_puzzle):
        st.write(i)
        col[count%3].write(str(i[1]+1)+' rotate '+str(i[2]))
        col[count%3].image(st.session_state.images[i[1]],width=200)

    if st.button('Replay'):
        for img in image_files:
            img_path = os.path.join(folder_path, img)
            image_placeholder.image(img_path, use_column_width=True)
            time.sleep(0.5) 
    
    if st.button('Save'):
        with open(st.session_state.project_name+'/solved_puzzle.json', 'w') as f:
            json.dump(st.session_state.solved_puzzle, f)
        st.success("Puzzle saved successfully!")

    if st.button('Next'):
        st.session_state.page=5
        st.rerun()
        
if st.session_state.page==5:
    filename = st.text_input("Enter comport to connect")

    if st.button('Connect'):
        if filename:
            try:
                st.session_state.arduino = serial.Serial(filename, 9600, timeout=1)
                time.sleep(2) 
                if st.session_state.is_open:
                    st.success(f"Successfully connected to {filename}")
                else:
                    st.error(f"Failed to connect to {filename}")
            except serial.SerialException as e:
                st.error(f"Failed to connect to {filename}. Error: {e}")
        else:
            st.error("Please enter a valid COM port.")
        
    if st.button('Next'):
        st.session_state.page=6
        st.session_state.id=0
        st.rerun()

if st.session_state.page==6:
    if 'id' not in st.session_state:
        st.session_state.id=0
    st.title('Place Blocks')
    st.write(f'Step {st.session_state.id+1}')
    if st.session_state.solved_puzzle[st.session_state.id][2]!=0:
        st.write(f'Rotate the block {st.session_state.solved_puzzle[st.session_state.id][2]*90}')
    else:
        st.write("No rotation need")

    st.write(f"Place Block in postion {st.session_state.id+1}")
    st.image(display_images(st.session_state.solved_puzzle[st.session_state.id][0]))
    
    if st.button('Lets Go'):
        if 'arduino' in st.session_state:
            st.session_state.arduino.write(b'Go to postion 1')

        st.write('done')
        st.session_state.id+=1
        st.rerun()
    
        