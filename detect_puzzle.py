def detect_puzzle(circle_tracks,vertical_line_tracks,horizontal_line_tracks,circle_colors):
    pos=[0,0,0,0]
    x_values=[x[0] for x in circle_tracks]
    if len(vertical_line_tracks)>0:
        x_values.append(vertical_line_tracks[0][0])

        min_index = x_values.index(min(x_values))
        if min_index<2:
            if circle_colors[min_index]==0:
                pos[0]=1
            else:
                pos[0]=-1
        max_index = x_values.index(max(x_values))
        if len(vertical_line_tracks)+len(horizontal_line_tracks)==2:
            if max_index<2:
                if circle_colors[max_index]==0:
                    pos[2]=1
                else:
                    pos[2]=-1
        else:
            if max_index<=2:
                if circle_colors[max_index]==0:
                    pos[2]=1
                else:
                    pos[2]=-1
    else:
        min_index = x_values.index(min(x_values))
        if circle_colors[min_index]==0:
            pos[0]=1
        else:
            pos[0]=-1
        max_index = x_values.index(max(x_values))
        
        if circle_colors[max_index]==0:
            pos[2]=1
        else:
            pos[2]=-1
    y_values=[x[1] for x in circle_tracks]
    if len(horizontal_line_tracks)>0:
        y_values.append(horizontal_line_tracks[0][1])
        
        min_index = y_values.index(min(y_values))
        if min_index<2:
            if circle_colors[min_index]==0:
                pos[1]=1
            else:
                pos[1]=-1
        max_index = y_values.index(max(y_values))
        if max_index<2:
            if circle_colors[max_index]==0:
                pos[3]=1
            else:
                pos[3]=-1
    else:
        min_index = y_values.index(min(y_values))
        if circle_colors[min_index]==0:
            pos[1]=1
        else:
            pos[1]=-1
        max_index = y_values.index(max(y_values))
        
        if circle_colors[max_index]==0:
            pos[3]=1
        else:
            pos[3]=-1
    # Print the index
    return pos