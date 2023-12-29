from customtkinter import *
from PIL import Image
from metadata_functions import get_video_metadata as video
from platform import system
import cv2

colors = ["#1C1C1C" , "#282828"]

def metadata_parser(metadatas):
    txt = ""
    try :
        for e in metadatas :
            if e != "Full" : txt += str(e)+" : "+str(metadatas[e])+"\n"
    except :
        txt = "There is no metadata in this file.\nTry another one."
    return txt

def extract_frames(video_path):

    clip = cv2.VideoCapture(video_path)
    total_frames = int(clip.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_to_extract = sorted(set(int(i * (total_frames / 8)) for i in range(8)))
    
    thumbnails = []

    for i in frames_to_extract :
        clip.set(cv2.CAP_PROP_POS_FRAMES, i)
        _, image = clip.read()
        try :
            thumbnails.append(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        except : 
            continue

    return thumbnails

def create_thumbnailer(thumbnails_list):
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
    img_size = img.size
    panel_size = (panel.winfo_width()-20, panel.winfo_height()-20)
    img_ratio = img_size[0]/img_size[1]
    panel_ratio = panel_size[0]/panel_size[1]
        
    if img_ratio <= panel_ratio :
        return (round(panel_size[1]*img_ratio), panel_size[1])
    else :
        return (panel_size[0], panel_size[0]//img_ratio)

def main(file):
    
    set_appearance_mode("dark")
    metadatas = video(file)
    txt = metadata_parser(metadatas)
    
    thumbnails = extract_frames(file)
    img = create_thumbnailer(thumbnails)
    
    root = CTkToplevel()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}+0+0')
    if system() == "Linux":root.attributes('-zoomed', True)
    else : root.state("zoomed")
    root.attributes('-topmost', True)
    
    frame = CTkFrame(root, fg_color=colors[0])
    frame.pack(fill=BOTH, expand=True)
    frame.grid_rowconfigure(0, weight=1, uniform="row")
    frame.grid_columnconfigure([0,1], weight=1, uniform='col')
        
    data_panel = CTkLabel(frame, bg_color=colors[1], text=txt, anchor=NW, justify=LEFT, padx=20, pady=20)
    data_panel.grid(column=0, rowspan=2, sticky=NSEW, padx = 30, pady=30)
    data_panel.update()
    data_panel.configure(wraplength = data_panel.winfo_width()-100)
    
    preview_panel = CTkLabel(frame, bg_color=colors[1], text='')
    preview_panel.grid(row=0, column=1, sticky=NSEW,  padx = 30, pady=30)

    preview_panel.update()
    size = fit(img, preview_panel)
    img = CTkImage(light_image=img, dark_image=img, size=size)
    preview_panel.configure(image=img, anchor=CENTER, padx=0, pady=0)

    if txt == "There is no metadata in this file.\nTry another one." :
        data_panel.configure(justify=CENTER, anchor=CENTER)

    root.title("Video metadata")
    root.mainloop()