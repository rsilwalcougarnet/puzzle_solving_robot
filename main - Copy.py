import cv2
import numpy as np

# Open the camera (default is 0, which is usually the default webcam)
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# A list to store circle details with their count and absence count
circle_tracks = []  # Each element will be [x, y, r, count, absent_count]

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    # Crop the frame if needed
    cropped_frame = frame[50:450, 230:600]

    rotated_frame = cv2.transpose(cropped_frame)  # Transpose the image (swap rows and columns)
    #rotated_frame = cv2.flip(rotated_frame, flipCode=1)  # Flip horizontally to complete the -90 degree rotation

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to create a binary mask (white and black)
    _, masked_frame = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)

    # Use HoughCircles to find circles in the masked frame
    circles = cv2.HoughCircles(masked_frame, 
                                cv2.HOUGH_GRADIENT, dp=1.6, minDist=30, 
                                param1=100, param2=20, minRadius=15, maxRadius=30)

    # If some circles are detected
    if circles is not None:
        # Convert the coordinates to integers
        circles = np.round(circles[0, :]).astype("int")

        # Iterate over each detected circle
        for (x, y, r) in circles:
            # Check if this circle's center is inside any existing circle
            is_inside = False
            for i, track in enumerate(circle_tracks):
                track_x, track_y, track_r, track_count, absent_count = track
                distance = np.sqrt((x - track_x)**2 + (y - track_y)**2)

                if distance < track_r:
                    # The current circle is inside an existing circle, reset its counter
                    circle_tracks[i][3] +=1 # Reset count for the circle
                    circle_tracks[i][4] = 0  # Reset absent count
                    is_inside = True
                    break

            # If the circle was not inside any other, track it
            if not is_inside:
                found = False
                for track in circle_tracks:
                    track_x, track_y, track_r, track_count, track_absent_count = track
                    if abs(x - track_x) < 10 and abs(y - track_y) < 10 and abs(r - track_r) < 10:
                        track[3] += 1  # Increment the counter for the circle
                        track[4] = 0  # Reset the absent count when it's detected
                        found = True
                        break
                
                if not found:
                    print('new_circle found')
                    circle_tracks.append([x, y, r, 1, 0])  # Start a new track for the circle

    # Update absence count for circles not detected in this iteration
    for i in range(len(circle_tracks)):
        if circle_tracks[i][4] < 10:
            circle_tracks[i][4] += 1  # Increment the absent count if not detected
        else:
            # Remove the circle if it's been absent for more than 10 iterations
            del circle_tracks[i]
            break  # Break after removal to avoid index shift during iteration

    # Iterate through tracked circles and check their colors if tracked for more than 30 frames
    for track in circle_tracks:
        track_x, track_y, track_r, track_count, track_absent_count = track
        # Draw the circle in the output image (Green color)
        cv2.circle(rotated_frame, (track_x, track_y), track_r, (0, 255, 0), 4)
        # Draw the center of the circle (Red color)
        cv2.circle(rotated_frame, (track_x, track_y), 2, (0, 0, 255), 3)

        # If the circle has been tracked for more than 30 frames
        if track_count > 30:
            # Create a mask with the appropriate size for the circle
            mask = np.zeros((track_r*2, track_r*2), dtype=np.uint8)
            cv2.circle(mask, (track_r, track_r), track_r, 255, thickness=-1)  # Create a white circle in the mask

            # Extract the region inside the circle from the original image
            # First, create a square image of the same size as the mask
            y_min = track_y - track_r//2
            y_max = track_y + track_r//2
            x_min =track_x - track_r//2
            x_max = track_x + track_r//2

            # Extract the region of interest (ROI) from the frame
            cropped_region = masked_frame[y_min:y_max, x_min:x_max]

            # Count the black and white pixels in the circle region
            black_pixels = np.sum(cropped_region < 100)   # Count black pixels (value 0)
            white_pixels = np.sum(cropped_region >100)  # Count white pixels (value 255)

            # Determine if the circle is mostly black or white
            if black_pixels > white_pixels:
                # Output "Black" (Circle is predominantly black)
                cv2.putText(rotated_frame, "Black", (track_x - 20, track_y - track_r - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)  # Text color black
            else:
                # Output "White" (Circle is predominantly white)
                cv2.putText(rotated_frame, "White", (track_x - 20, track_y - track_r - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)  # Text color white


    # Display the resulting frames
    cv2.imshow('Camera Feed with Circles', rotated_frame)
    cv2.imshow('Masked Frame', masked_frame)

    # Wait for the user to press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close the display window
cap.release()
cv2.destroyAllWindows()
