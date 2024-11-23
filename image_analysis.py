import numpy as np

def line_analysis(lines,vertical_line_tracks,horizontal_line_tracks):
    if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]

                # Calculate the slope of the line (if x2 - x1 is not zero)
                if x2 - x1 != 0:
                    slope = (y2 - y1) / (x2 - x1)
                else:
                    slope = np.inf  # vertical line (infinite slope)

                # Classify the line as vertical or horizontal based on slope
                if abs(slope) > 5:  # roughly vertical
                    # Track vertical lines (group lines with similar x-values)
                    is_vertical_overlapping = False
                    for i, track in enumerate(vertical_line_tracks):
                        vx1, vy1, vx2, vy2, count, absent_count = track
                        # Check if the x-coordinates are close (within a tolerance)
                        if abs(x1 - vx1) < 20 or abs(x2 - vx2) < 20:
                            vertical_line_tracks[i][4] += 1  # Increment the line count
                            vertical_line_tracks[i][5] = 0  # Reset absent count
                            is_vertical_overlapping = True
                            break

                    if not is_vertical_overlapping:
                        vertical_line_tracks.append([x1, 0, x2, 500, 1, 0])  # Start a new track for vertical line

                elif abs(slope) < 0.2:  # roughly horizontal
                    # Track horizontal lines (group lines with similar y-values)
                    is_horizontal_overlapping = False
                    for i, track in enumerate(horizontal_line_tracks):
                        hx1, hy1, hx2, hy2, count, absent_count = track
                        # Check if the y-coordinates are close (within a tolerance)
                        if abs(y1 - hy1) < 20 or abs(y2 - hy2) < 20:
                            horizontal_line_tracks[i][4] += 1  # Increment the line count
                            horizontal_line_tracks[i][5] = 0  # Reset absent count
                            is_horizontal_overlapping = True
                            break

                    if not is_horizontal_overlapping:
                        horizontal_line_tracks.append([0, y1, 500, y2, 1, 0])  # Start a new track for horizontal line

    # Update absence count for lines not detected in this iteration
    for i in range(len(vertical_line_tracks)):
        if vertical_line_tracks[i][5] < 5:
            vertical_line_tracks[i][5] += 1  # Increment the absent count if not detected
        else:
            del vertical_line_tracks[i]  # Remove line if absent for more than 10 iterations
            break  # Break after removal to avoid index shift during iteration

    for i in range(len(horizontal_line_tracks)):
        if horizontal_line_tracks[i][5] < 5:
            horizontal_line_tracks[i][5] += 1  # Increment the absent count if not detected
        else:
            del horizontal_line_tracks[i]  # Remove line if absent for more than 10 iterations
            break  # Break after removal to avoid index shift during iteration

    return vertical_line_tracks,horizontal_line_tracks

def circle_analysis(circles,circle_tracks):
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
                    circle_tracks.append([x, y, r, 1, 0])  # Start a new track for the circle

    # Update absence count for circles not detected in this iteration
    for i in range(len(circle_tracks)):
        if circle_tracks[i][4] < 3:
            circle_tracks[i][4] += 1  # Increment the absent count if not detected
        else:
            # Remove the circle if it's been absent for more than 10 iterations
            del circle_tracks[i]
            break  # Break after removal to avoid index shift during iteration
    return circle_tracks