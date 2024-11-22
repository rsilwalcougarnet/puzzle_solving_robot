import streamlit as st
from main import Camera
import streamlit as st
import cv2
import numpy as np
if 'camera' not in st.session_state:
    st.session_state.camera = Camera()
    st.session_state.puzzle=[]
    st.session_state.pos=[0,0,0,0]
    st.session_state.images=[]

import streamlit as st

from camera_input_live import camera_input_live

image = camera_input_live()
col1,col2=st.columns(2)
if image:
    # To read image file buffer with OpenCV:
    bytes_data = image.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    rotated_frame, masked_frame, edges, pos=st.session_state.camera.get_frame(cv2_img)
    col1.image(rotated_frame)
    col2.image(edges)
    if sum([1 for i in pos if i==0])<3:
        st.session_state.pos=pos
    st.write(st.session_state.pos)

    if st.button('next'):
        if sum([1 for i in st.session_state.pos if i==0])>=3:
            st.write('not allowed')
        else:
            st.session_state.images.append(edges)
            st.session_state.puzzle.append(st.session_state.pos)
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
        


