from metadata_window import Window
from customtkinter import CENTER, CTkImage
from PIL import Image
from metadata_functions import get_video_metadata as video
import cv2

def metadata_parser(metadatas):
    """Parse the metadatas from a dictionnary to a text to display on the page
    Args:
        metadatas (dict): Dictionnairy containing the metadatas
    Returns:
        str: Pretty printing of the metadatas
    """
    txt = ""
    try :
        for e in metadatas :
            txt += str(e)+" : "+str(metadatas[e])+"\n"
    except :
        txt = "There is no metadata in this file.\nTry another one."
    return txt

def extract_frames(video_path):
    """Extract 8 frames at different regularly spaced from the video to create a relevant thumbnail
    Args:
        video_path (str): The path of the video
    Returns:
        list: A list of the 8 frames as PIL Images 
    """
    
    # Get the number of the interesting frames to extracts    
    clip = cv2.VideoCapture(video_path)
    total_frames = int(clip.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_to_extract = sorted(set(int(i * (total_frames / 8)) for i in range(8)))
    
    thumbnails = []

    # Extract the thumbnails and stores it in a list
    for i in frames_to_extract :
        clip.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, image = clip.read()
        try :
            thumbnails.append(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        except : 
            continue

    return thumbnails

def create_thumbnailer(thumbnails_list):
    """Create a beautiful thumbnailer through a grid of 4x2 images

    Args:
        thumbnails_list (list): List of 8 PIL Images composing the thumbnailer

    Returns:
        PIL Image: The final Image composed of all the thumbnails
    """    
    grid_width = 2
    grid_height = 4
    thumbnail_size = thumbnails_list[0].size
    final_image = Image.new('RGB', (grid_width * thumbnail_size[0], grid_height * thumbnail_size[1]))

    for i in range(grid_height):
        for j in range(grid_width):
            index = i*grid_width + j
            image = thumbnails_list[index]
            final_image.paste(image, (j * thumbnail_size[0], i * thumbnail_size[1]))

    return final_image

def fit(img, panel):
    """Find the best size to fit the best as possible an image into the preview panel, keeping the image aspect ratio
    Args:
        img (PIL Image): The image to fit into the panel
        panel (CTkLabel): The panel
    Returns:
        Tuple: The size (width, height) of the image to fit it in the panel
    """
    img_size = img.size
    panel_size = (panel.winfo_width()-20, panel.winfo_height()-20)
    img_ratio = img_size[0]/img_size[1]
    panel_ratio = panel_size[0]/panel_size[1]
        
    if img_ratio <= panel_ratio :
        return (round(panel_size[1]*img_ratio), panel_size[1])
    else :
        return (panel_size[0], panel_size[0]//img_ratio)

def main(file):
    """Create the window displaying the metadatas
    Args:
        file (str): The path to the file to analyse
    """
    
    metadatas = video(file)
    txt = metadata_parser(metadatas)
    
    # Create the thumbnailer from the video
    thumbnails = extract_frames(file)
    img = create_thumbnailer(thumbnails)
    
    # Create the window with 2 panel : data and preview
    win = Window(n_panel=2, title="Video metadatas")

    win.preview_panel.update()
    size = fit(img, win.preview_panel)
    img = CTkImage(light_image=img, dark_image=img, size=size)
    
    win.data_panel.configure(state='normal')
    win.data_panel.insert('1.0', txt)
    win.data_panel.configure(state='disabled')
    win.preview_panel.configure(image=img, anchor=CENTER, padx=0, pady=0)    

    win.root.mainloop()