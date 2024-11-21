import cv2
import numpy as np
from detect_puzzle import detect_puzzle
from image_analysis import line_analysis,circle_analysis

def draw_features_items(rotated_frame,circle_tracks,vertical_line_tracks,horizontal_line_tracks):
    for track in circle_tracks:
        track_x, track_y, track_r, track_count, track_absent_count = track
        cv2.circle(rotated_frame, (track_x, track_y), track_r, (0, 255, 0), 4)
        cv2.circle(rotated_frame, (track_x, track_y), 2, (0, 0, 255), 3)

    for track in vertical_line_tracks:
        x1, y1, x2, y2, count, absent_count = track
        cv2.line(rotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 3)  # Green for vertical lines

    for track in horizontal_line_tracks:
        x1, y1, x2, y2, count, absent_count = track
        cv2.line(rotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 3)  # Blue for horizontal lines
    return rotated_frame

def label_cricles(rotated_frame,masked_frame,circle_tracks,circle_colors=[]):
    for track in circle_tracks:
        track_x, track_y, track_r, track_count, track_absent_count = track
        if track_count > 30:

            y_min = track_y - track_r//2
            y_max = track_y + track_r//2
            x_min =track_x - track_r//2
            x_max = track_x + track_r//2

            cropped_region = masked_frame[y_min:y_max, x_min:x_max]

            black_pixels = np.sum(cropped_region < 100)  
            white_pixels = np.sum(cropped_region >100)  
            if black_pixels > white_pixels:
                # Output "Black" (Circle is predominantly black)
                cv2.putText(rotated_frame, "Black", (track_x - 20, track_y - track_r - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)  # Text color black
                circle_colors.append(0)
            else:
                # Output "White" (Circle is predominantly white)
                cv2.putText(rotated_frame, "White", (track_x - 20, track_y - track_r - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)  # Text color white
                circle_colors.append(1)
    return rotated_frame,circle_colors
# Open the camera (default is 0, which is usually the default webcam)
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# A list to store circle details with their count and absence count
circle_tracks = []  # Each element will be [x, y, r, count, absent_count]
vertical_line_tracks=[]
horizontal_line_tracks=[]
counter=0
ready_status=False
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    cropped_frame = frame[50:450, 230:600]
    rotated_frame = cv2.transpose(cropped_frame)  
    gray_frame = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2GRAY)
    _, masked_frame = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(masked_frame, 100, 20, apertureSize=3)
    
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=100, maxLineGap=10)

    circles = cv2.HoughCircles(masked_frame, 
                                cv2.HOUGH_GRADIENT, dp=1.6, minDist=30, 
                                param1=100, param2=20, minRadius=15, maxRadius=30)

    circle_tracks=circle_analysis(circles,circle_tracks)

    rotated_frame,circle_colors=label_cricles(rotated_frame,masked_frame,circle_tracks,[])


    
    vertical_line_tracks,horizontal_line_tracks=line_analysis(lines,vertical_line_tracks,horizontal_line_tracks)
    
    rotated_frame=draw_features_items(rotated_frame,circle_tracks,vertical_line_tracks,horizontal_line_tracks)

    
    if len(vertical_line_tracks)+len(horizontal_line_tracks)+len(circle_tracks)==4 and (len(circle_colors)== len(circle_tracks)):
        counter+=1
        if counter>40:
            ready_status=True
            cv2.putText(rotated_frame, "Ready", (40,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)  # Text color black
    else:
        ready_status=False
        counter=0
    pos=[0,0,0,0]
    if ready_status:
        pos=detect_puzzle(circle_tracks,vertical_line_tracks,horizontal_line_tracks,circle_colors)
        print(pos)
    # Display the resulting frames
    cv2.imshow('Camera Feed with Circles and Lines', rotated_frame)
    cv2.imshow('Masked Frame', masked_frame)
    cv2.imshow('edges', edges)
    cv2.imshow('Masked Frame', masked_frame)
    # Wait for the user to press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the capture object and close the display window
cap.release()
cv2.destroyAllWindows()
