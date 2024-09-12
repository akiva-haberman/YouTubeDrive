import os 
import cv2
from PIL import Image 
from encode import get_new_file_name

FPS = 2

def generate_video(): 
    image_folder = 'outDir' # make sure to use your folder 
    video_name = get_new_file_name('mygeneratedvideo','avi')
    
    images = [img for img in os.listdir(image_folder) 
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 
    images.sort()
     
    # Array images should only consider 
    # the image files ignoring others if any   
    frame = cv2.imread(os.path.join(image_folder, images[0])) 
  
    # setting the frame width, height width 
    # the width, height of first image 
    height, width, layers = frame.shape   
    fourcc = cv2.VideoWriter.fourcc(*list('Y444'))
  
    video = cv2.VideoWriter(video_name, 0, 0, (width, height))  
  
    # Appending the images to the video one by one 
    for image in images:  
        video.write(cv2.imread(os.path.join(image_folder, image)))  
      
    # Deallocating memories taken for window creation 
    cv2.destroyAllWindows()  
    video.release()  # releasing the video generated 

generate_video()

