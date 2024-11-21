import random
import numpy as np
import time
import os
import shutil
import uuid
from PIL import Image
from datetime import datetime
import time




from drawing_tools import create_large_image

def manage_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder if it does not exist
        os.makedirs(folder_path)
        print(f"Folder created at: {folder_path}")
    else:
        # Folder exists, delete all files inside it
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)  # Delete the file
        print(f"All files deleted in folder: {folder_path}")

def rotate(pieces):
    return [pieces[-1],pieces[0],pieces[1],pieces[2]]



def solve(Puzzle,side_pieces,corner_pieces,name="project_name",main_func=False):

    if main_func:
        manage_folder(name)


    large_image = create_large_image(Puzzle)
    time.sleep(0.01)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    milliseconds = f"{datetime.now().microsecond // 1000:03d}"  # Capture milliseconds (3 digits)

    # Combine the current time with milliseconds for a unique file name
    file_name = name+f"/output_image_{current_time}_{milliseconds}.png"
    large_image.save(file_name)

    if [] not in Puzzle:
        print("Finished")

        return True,Puzzle


    if len(Puzzle[3])==0:
        for selected_conrner_piece in side_pieces:
            if selected_conrner_piece[0][2]+Puzzle[4][0][0]==0 and selected_conrner_piece[0][2]!=0 and selected_conrner_piece[0][0]==0:
                temp=side_pieces.copy()
                temp.remove(selected_conrner_piece)
                Puzzle_temp=Puzzle.copy()
                Puzzle_temp[3]=selected_conrner_piece
                finished,solved_puzzle=solve(Puzzle_temp,temp,corner_pieces,name)
                if finished:
                    return True,solved_puzzle

            original_selected_conrner_piece=selected_conrner_piece.copy()
            for i in range(3):
                selected_conrner_piece=[rotate(selected_conrner_piece[0]),selected_conrner_piece[1],selected_conrner_piece[2]+1]
                if selected_conrner_piece[0][2]+Puzzle[4][0][0]==0 and selected_conrner_piece[2]<=4 and selected_conrner_piece[0][2]!=0 and selected_conrner_piece[0][0]==0:
                    temp=side_pieces.copy()
                    temp.remove(original_selected_conrner_piece)
                    Puzzle_temp=Puzzle.copy()
                    Puzzle_temp[3]=selected_conrner_piece
                    finished,solved_puzzle=solve(Puzzle_temp,temp,corner_pieces,name)
                    if finished:
                        return True,solved_puzzle

    if len(Puzzle[3])!=0 and len(Puzzle[0])==0:
        for selected_conrner_piece in corner_pieces:
            if selected_conrner_piece[0][3]+Puzzle[3][0][1]==0 and selected_conrner_piece[0][0]==0 and selected_conrner_piece[0][1]==0:
                temp=corner_pieces.copy()
                temp.remove(selected_conrner_piece)
                Puzzle_temp=Puzzle.copy()
                Puzzle_temp[0]=selected_conrner_piece
                finished,solved_puzzle=solve(Puzzle_temp,side_pieces,temp,name)
                if finished:
                    return True,solved_puzzle

            original_selected_conrner_piece=selected_conrner_piece.copy()
            for i in range(3):
                selected_conrner_piece=[rotate(selected_conrner_piece[0]),selected_conrner_piece[1],selected_conrner_piece[2]+1]
                if selected_conrner_piece[0][3]+Puzzle[3][0][1]==0 and selected_conrner_piece[2]<=4 and selected_conrner_piece[0][0]==0 and selected_conrner_piece[0][1]==0:
                    temp=corner_pieces.copy()
                    temp.remove(original_selected_conrner_piece)
                    Puzzle_temp=Puzzle.copy()
                    Puzzle_temp[0]=selected_conrner_piece
                    finished,solved_puzzle=solve(Puzzle_temp,side_pieces,temp,name)
                    if finished:
                        return True,solved_puzzle

    if len(Puzzle[3])!=0 and len(Puzzle[0])!=0 and len(Puzzle[1])==0:

        for selected_conrner_piece in side_pieces:
            if selected_conrner_piece[0][3]+Puzzle[4][0][1]==0 and selected_conrner_piece[0][0]+Puzzle[0][0][2]==0 and selected_conrner_piece[0][1]==0 :
                temp=side_pieces.copy()
                temp.remove(selected_conrner_piece)
                Puzzle_temp=Puzzle.copy()
                Puzzle_temp[1]=selected_conrner_piece
                finished,solved_puzzle=solve(Puzzle_temp,temp,corner_pieces,name)
                if finished:
                    return True,solved_puzzle
            original_selected_conrner_piece=selected_conrner_piece.copy()
            for i in range(3):
                selected_conrner_piece=[rotate(selected_conrner_piece[0]),selected_conrner_piece[1],selected_conrner_piece[2]+1]
                if selected_conrner_piece[0][3]+Puzzle[4][0][1]==0 and selected_conrner_piece[0][0]+Puzzle[0][0][2]==0 and selected_conrner_piece[0][1]==0:
                    temp=side_pieces.copy()
                    temp.remove(original_selected_conrner_piece)
                    Puzzle_temp=Puzzle.copy()
                    Puzzle_temp[1]=selected_conrner_piece
                    finished,solved_puzzle=solve(Puzzle_temp,temp,corner_pieces,name)
                    if finished:
                        return True,solved_puzzle


    if len(Puzzle[3])!=0 and len(Puzzle[0])!=0 and len(Puzzle[1])!=0 and len(Puzzle[2])==0:
        for selected_conrner_piece in corner_pieces:
            if selected_conrner_piece[0][0]+Puzzle[1][0][2]==0 and selected_conrner_piece[0][1]==0 and selected_conrner_piece[0][2]==0:
                temp=corner_pieces.copy()
                temp.remove(selected_conrner_piece)
                Puzzle_temp=Puzzle.copy()
                Puzzle_temp[2]=selected_conrner_piece
                finished,solved_puzzle=solve(Puzzle_temp,side_pieces,temp,name)
                if finished:
                    return True,solved_puzzle

            original_selected_conrner_piece=selected_conrner_piece.copy()
            for i in range(3):
                selected_conrner_piece=[rotate(selected_conrner_piece[0]),selected_conrner_piece[1],selected_conrner_piece[2]+1]
                if selected_conrner_piece[0][0]+Puzzle[1][0][2]==0 and selected_conrner_piece[2]<=4  and selected_conrner_piece[0][1]==0 and selected_conrner_piece[0][2]==0:
                    temp=corner_pieces.copy()
                    temp.remove(original_selected_conrner_piece)
                    Puzzle_temp=Puzzle.copy()
                    Puzzle_temp[2]=selected_conrner_piece
                    finished,solved_puzzle=solve(Puzzle_temp,side_pieces,temp,name)
                    if finished:
                        return True,solved_puzzle


    if len(Puzzle[3])!=0 and len(Puzzle[0])!=0 and len(Puzzle[1])!=0 and len(Puzzle[2])!=0 and len(Puzzle[5])==0:
        for selected_conrner_piece in side_pieces:
            if selected_conrner_piece[0][0]+Puzzle[4][0][2]==0 and selected_conrner_piece[0][1]+Puzzle[2][0][3]==0:
                temp=side_pieces.copy()
                temp.remove(selected_conrner_piece)
                Puzzle_temp=Puzzle.copy()
                Puzzle_temp[5]=selected_conrner_piece
                finished,solved_puzzle=solve(Puzzle_temp,temp,corner_pieces,name)
                if finished:
                    return True,solved_puzzle
            original_selected_conrner_piece=selected_conrner_piece.copy()
            for i in range(3):
                selected_conrner_piece=[rotate(selected_conrner_piece[0]),selected_conrner_piece[1],selected_conrner_piece[2]+1]
                if selected_conrner_piece[0][0]+Puzzle[4][0][2]==0 and selected_conrner_piece[0][1]+Puzzle[2][0][3]==0:
                    temp=side_pieces.copy()
                    temp.remove(original_selected_conrner_piece)
                    Puzzle_temp=Puzzle.copy()
                    Puzzle_temp[5]=selected_conrner_piece
                    finished,solved_puzzle=solve(Puzzle_temp,temp,corner_pieces,name)
                    if finished:
                        return True,solved_puzzle

    if len(Puzzle[3])!=0 and len(Puzzle[0])!=0 and len(Puzzle[1])!=0 and len(Puzzle[2])!=0 and len(Puzzle[5])!=0 and len(Puzzle[8])==0:
       for selected_conrner_piece in corner_pieces:
            if selected_conrner_piece[0][1]+Puzzle[5][0][3]==0:
                temp=corner_pieces.copy()
                temp.remove(selected_conrner_piece)
                Puzzle_temp=Puzzle.copy()
                Puzzle_temp[8]=selected_conrner_piece
                finished,solved_puzzle=solve(Puzzle_temp,side_pieces,temp,name)
                if finished:
                    return True,solved_puzzle

            original_selected_conrner_piece=selected_conrner_piece.copy()
            for i in range(3):
                selected_conrner_piece=[rotate(selected_conrner_piece[0]),selected_conrner_piece[1],selected_conrner_piece[2]+1]
                if selected_conrner_piece[0][1]+Puzzle[5][0][3]==0:
                    temp=corner_pieces.copy()
                    temp.remove(original_selected_conrner_piece)
                    Puzzle_temp=Puzzle.copy()
                    Puzzle_temp[8]=selected_conrner_piece
                    finished,solved_puzzle=solve(Puzzle_temp,side_pieces,temp,name)
                    if finished:
                        return True,solved_puzzle

    if len(Puzzle[3])!=0 and len(Puzzle[0])!=0 and len(Puzzle[1])!=0 and len(Puzzle[2])!=0 and len(Puzzle[5])!=0 and len(Puzzle[6])==0:
        print(corner_pieces)
        for selected_conrner_piece in corner_pieces:
            if selected_conrner_piece[0][1]+Puzzle[3][0][3]==0 and selected_conrner_piece[0][0]==0 and selected_conrner_piece[0][-1]==0:
                temp=corner_pieces.copy()
                temp.remove(selected_conrner_piece)
                Puzzle_temp=Puzzle.copy()
                Puzzle_temp[6]=selected_conrner_piece
                finished,solved_puzzle=solve(Puzzle_temp,side_pieces,temp,name)
                if finished:
                    return True,solved_puzzle

            original_selected_conrner_piece=selected_conrner_piece.copy()
            for i in range(3):
                selected_conrner_piece=[rotate(selected_conrner_piece[0]),selected_conrner_piece[1],selected_conrner_piece[2]+1]
                if selected_conrner_piece[0][1]+Puzzle[3][0][3]==0 and selected_conrner_piece[0][0]==0 and selected_conrner_piece[0][-1]==0:
                    temp=corner_pieces.copy()
                    temp.remove(original_selected_conrner_piece)
                    Puzzle_temp=Puzzle.copy()
                    Puzzle_temp[6]=selected_conrner_piece
                    finished,solved_puzzle=solve(Puzzle_temp,side_pieces,temp,name)
                    if finished:
                        return True,solved_puzzle

    if (len(Puzzle[7])==0 and len(Puzzle[8])!=0 and len(Puzzle[6])!=0 and len(Puzzle[3])!=0 and len(Puzzle[5])!=0):
        print(side_pieces)
        for selected_conrner_piece in side_pieces:

            if selected_conrner_piece[0][0]+Puzzle[6][0][2]==0 and selected_conrner_piece[0][-1]==0:

                temp=side_pieces.copy()
                temp.remove(selected_conrner_piece)
                Puzzle_temp=Puzzle.copy()
                Puzzle_temp[7]=selected_conrner_piece
                finished,solved_puzzle=solve(Puzzle_temp,temp,corner_pieces,name)

                if finished:
                    return True,solved_puzzle
            original_selected_conrner_piece=selected_conrner_piece.copy()
            for i in range(3):
                selected_conrner_piece=[rotate(selected_conrner_piece[0]),selected_conrner_piece[1],selected_conrner_piece[2]+1]
                if selected_conrner_piece[0][0]+Puzzle[6][0][2]==0 and selected_conrner_piece[0][-1]==0:
                    temp=side_pieces.copy()
                    temp.remove(original_selected_conrner_piece)
                    Puzzle_temp=Puzzle.copy()
                    Puzzle_temp[7]=selected_conrner_piece
                    finished,solved_puzzle=solve(Puzzle_temp,temp,corner_pieces,name)
                    if finished:
                        return True,solved_puzzle


    
    return False,[]


def puzzle_solver(pieces,name):
    corner_pieces=[]
    side_pieces=[]
    center_pieces=[]

    for count,piece in enumerate(pieces):
        if (len(np.where(np.array(piece)==0)[0]))==2:
            corner_pieces.append([piece,count,0])
        elif (len(np.where(np.array(piece)==0)[0]))==1:
            side_pieces.append([piece,count,0])
        else:
            center_pieces.append([piece,count,0])
    
    Puzzle=[[],[],[],[],[],[],[],[],[]]
    if len(center_pieces)!=1 and len(side_pieces)!=4 and len(corner_pieces)!=4:
        return Puzzle,{"message":"invalid puzzle"}
    
    Puzzle[4]=center_pieces[0]


    _, solved_puzzle = solve(Puzzle, side_pieces, corner_pieces,name,main_func=True)

    return solved_puzzle,{"message":"puzzle solved"}



if __name__=="__main__":
    pieces=[[0,0,-1,-1],[1,0,1,-1],[-1,0,0,1],[0,1,-1,1],[-1,-1,1,1],[1,-1,0,-1],[0,-1,1,0],[-1,1,-1,0],[1,1,0,0]]
    corner_pieces=[]
    side_pieces=[]
    center_pieces=[]

    for count,piece in enumerate(pieces):
        if (len(np.where(np.array(piece)==0)[0]))==2:
            corner_pieces.append([piece,count,0])
        elif (len(np.where(np.array(piece)==0)[0]))==1:
            side_pieces.append([piece,count,0])
        else:
            center_pieces.append([piece,count,0])

    center_pieces[0]

    Puzzle=[[],[],[],[],[],[],[],[],[]]

    Puzzle[4]=center_pieces[0]


    _, solved_puzzle = solve(Puzzle, side_pieces, corner_pieces,name="first_project",main_func=True)

    