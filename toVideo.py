import os 
import opencv4
from PIL import Image 

def generate_video(): 
    image_folder = '.' # make sure to use your folder 
    video_name = 'mygeneratedvideo.avi'
    os.chdir("C:\\Python\\Geekfolder2") 
      
    images = [img for img in os.listdir(image_folder) 
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 
     
    # Array images should only consider 
    # the image files ignoring others if any 
    print(images)  
  
    frame = opencv.imread(os.path.join(image_folder, images[0])) 
  
    # setting the frame width, height width 
    # the width, height of first image 
    height, width, layers = frame.shape   
  
    video = opencv.VideoWriter(video_name, 0, 1, (width, height))  
  
    # Appending the images to the video one by one 
    for image in images:  
        video.write(opencv.imread(os.path.join(image_folder, image)))  
      
    # Deallocating memories taken for window creation 
    opencv.destroyAllWindows()  
    video.release()  # releasing the video generated 