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

def label_circles(rotated_frame,masked_frame,circle_tracks,circle_colors=[]):
    for track in circle_tracks:
        track_x, track_y, track_r, track_count, track_absent_count = track
        if track_count > 2:

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

import cv2
import numpy as np

class Camera:
    def __init__(self):
        #self.cap = cv2.VideoCapture(0)
        self.circle_tracks = []  # List to store circle details with count and absence count
        self.vertical_line_tracks = []
        self.horizontal_line_tracks = []
        self.counter = 0
        self.ready_status = False
    
    def get_frame(self,frame):
        # Capture frame from camera
        #ret, frame = self.cap.read()
        
        # Crop and rotate the frame
        cropped_frame = frame[50:450, 280:650]
        rotated_frame = cv2.transpose(cropped_frame)
        
        # Convert to grayscale and apply binary threshold
        gray_frame = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2GRAY)
        _, masked_frame = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)
        
        # Detect edges using Canny
        edges = cv2.Canny(masked_frame, 100, 20, apertureSize=3)

        # Detect lines using Hough Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=10, minLineLength=100, maxLineGap=10)

        # Detect circles using Hough Transform
        circles = cv2.HoughCircles(masked_frame, 
                                    cv2.HOUGH_GRADIENT, dp=1.6, minDist=30, 
                                    param1=100, param2=20, minRadius=15, maxRadius=30)

        # Circle analysis and update circle tracks
        self.circle_tracks = circle_analysis(circles, self.circle_tracks)
        
        # Label circles with colors
        rotated_frame, circle_colors = label_circles(rotated_frame, masked_frame, self.circle_tracks, [])
        
        # Line analysis (vertical and horizontal lines)
        self.vertical_line_tracks, self.horizontal_line_tracks = line_analysis(lines, self.vertical_line_tracks, self.horizontal_line_tracks)
        
        # Draw features on the frame
        rotated_frame = draw_features_items(rotated_frame, self.circle_tracks, self.vertical_line_tracks, self.horizontal_line_tracks)

        # Check if the system is ready
        if len(self.vertical_line_tracks) + len(self.horizontal_line_tracks) + len(self.circle_tracks) == 4 and len(circle_colors) == len(self.circle_tracks):
            self.counter += 1
            if self.counter > 2:
                self.ready_status = True
                cv2.putText(rotated_frame, "Ready", (40, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)  # Text color black
        else:
            self.ready_status = False
            self.counter = 0
        
        pos = [0, 0, 0, 0]  # Default position
        if self.ready_status:
            pos = detect_puzzle(self.circle_tracks, self.vertical_line_tracks, self.horizontal_line_tracks, circle_colors)

        return rotated_frame, masked_frame, edges, pos
if __name__=="__main__":
    camera=Camera()# Display the resulting frames)
    while True:
        rotated_frame,masked_frame,edges,pos=camera.get_frame()

        # Display the resulting frames
        cv2.imshow('Camera Feed with Circles and Lines', rotated_frame)
        cv2.imshow('Masked Frame', masked_frame)
        cv2.imshow('edges', edges)
        cv2.imshow('Masked Frame', masked_frame)
        # Wait for the user to press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the capture object and close the display window
    camera.cap.release()
    cv2.destroyAllWindows()
