import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def transform_image(image, flip=False, rotate=0):

    if flip:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    image = image.rotate(rotate * 90, expand=True)
    
    return image

def display_images(input_values, img1=Image.open('drawing_features/curved_line.png'), img2=Image.open('drawing_features/st_line.png'), output_size=(450, 500)):
    
    images = []
    
    for i, input in enumerate(input_values):
        if input == 0: 
            images.append(transform_image(img2, flip=False, rotate=i))
            plt.imshow(images[0])
        elif input == 1:
            images.append(transform_image(img1, flip=False, rotate=i if i%2==0 else -i))
        elif input == -1:
            images.append(transform_image(img1, flip=True, rotate=i if i%2==0 else -i))
    
    
    left, top, right, bottom = images
    final_image = Image.new('RGB', output_size, (255, 255, 255))
    if input_values[0]==1:
        final_image.paste(left, (50, 80)) 
    elif input_values[0]==-1:
        final_image.paste(left, (70, 80))  
    
    else:
        final_image.paste(left, (110, 80)) 
      
    if input_values[1]==1:
        final_image.paste(top, (120, 20)) 
    elif input_values[1]==-1:
       final_image.paste(top, (115, 40)) 
    
    else:
        final_image.paste(top, (110, 80))  

    if input_values[2]==1:
        final_image.paste(right, (340, 90))  
    elif input_values[2]==-1:
       final_image.paste(right, (315, 85)) 
    
    else:
        final_image.paste(right, (370, 80))  

    if input_values[3]==1:
         final_image.paste(bottom, (115, 310))  
    elif input_values[3]==-1:
        final_image.paste(bottom, (115, 280))  
    
    else:
        final_image.paste(bottom, (105, 340))  
    return final_image.crop((60,30,430,400))



def transform_image(image, flip=False, rotate=0):
    if flip:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    image = image.rotate(rotate * 90, expand=True)  
    
    return image



def create_large_image(piece_instructions, piece_size=(370, 370), grid_size=(3, 3)):
    img1 = Image.open('drawing_features/curved_line.png')
    img2 = Image.open('drawing_features/st_line.png')
    
    large_image = Image.new('RGB', (370*3,370*3), (255, 255, 255))

    for i,piece in enumerate(piece_instructions):
        if piece==[]:
            continue
        else:
            # Calculate the row and column of the current piece in the 3x3 grid
            row = i // grid_size[1]
            col = i % grid_size[1]
            large_image.paste(display_images(piece[0], img1, img2), ( col*370, row*370)) 
    return large_image


if __name__=="__main__":
    

    solved_puzzle=[[[0, 0, 1, 1], 8, 2],
    [[-1, 0, -1, 1], 7, 2],
    [[1, 0, 0, -1], 6, 2],
    [[0, -1, 1, -1], 5, 2],
    [[-1, -1, 1, 1], 4, 0],
    [[-1, 1, 0, 1], 1, 1],
    [[0, 1, -1, 0], 2, 2],
    [[1, -1, 1, 0], 3, 3],
    [[-1, -1, 0, 0], 0, 2]]

    # Generate the large image with the puzzle pieces
    large_image = create_large_image(solved_puzzle)

    # Display the large image
    plt.imshow(large_image)
    plt.axis('off')  # Hide axes
    plt.show()
