from customtkinter import *
from PIL import Image
from metadata_functions import get_image_metadata as exif
import tkintermapview as tkmap

colors = ["#1C1C1C" , "#282828"]

def fit(img, panel):
    img_size = img.size
    panel_size = (panel.winfo_width(), panel.winfo_height())
    img_ratio = img_size[0]/img_size[1]
    panel_ratio = panel_size[0]/panel_size[1]
    
    if img_ratio <= panel_ratio :
        return (panel_size[1]*img_ratio, panel_size[1])
    else :
        return (panel_size[0], panel_size[0]//img_ratio)
    
def metadata_parser(metadatas):
    txt = ""
    tmp = "\n"
    try :
        for e in metadatas["Full"] :
            if str(metadatas["Full"][e])[:2] != "b'" and e != "GPSInfo":
                txt += str(e)+" : "+str(metadatas["Full"][e])+"\n"
    except :
        txt = "There is no metadata in this file.\nTry another one."
    try :
        for e in metadatas :
            if e != "Full": tmp += str(e)+" : "+str(metadatas[e])+"\n"
        txt += tmp
    except :
        txt += ""
                
    return txt

def main(file):
    
    set_appearance_mode("dark")

    img = Image.open(file)
    metadatas = exif(file)
    txt = metadata_parser(metadatas)
    
    root = CTkToplevel()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}+0+0')
    
    frame = CTkFrame(root, fg_color=colors[0])
    frame.pack(fill=BOTH, expand=True)
    frame.grid_rowconfigure([0,1], weight=1, uniform="row")
    frame.grid_columnconfigure([0,1], weight=1, uniform='col')
        
    data_panel = CTkLabel(frame, bg_color=colors[1], text=txt, anchor=NW, justify=LEFT, padx=20, pady=20)
    data_panel.grid(column=0, rowspan=2, sticky=NSEW, padx = 30, pady=30)
    data_panel.update()
    data_panel.configure(wraplength = data_panel.winfo_width() - 100)
    
    if txt == "There is no metadata in this file.\nTry another one." :
        data_panel.configure(justify=CENTER, anchor=CENTER)
    
    preview_panel = CTkLabel(frame, bg_color=colors[1], text='')
    preview_panel.grid(row=0, column=1, sticky=NSEW,  padx = 30, pady=30)
    
    preview_panel.update()
    size = fit(img, preview_panel)
    img = CTkImage(light_image=img, dark_image=img, size=size)
    preview_panel.configure(image=img, anchor=CENTER, padx=0, pady=0)    
    
    try :
        map_panel = tkmap.TkinterMapView(frame)
        map_panel.set_position(deg_x=metadatas["Coordinates"][0], deg_y=metadatas["Coordinates"][1], marker=True)
        map_panel.grid(row=1, column=1, sticky=NSEW,  padx = 30, pady=30)
    except :
        map_panel = CTkLabel(frame, bg_color=colors[1], text='Map is unavailable :\nThere is no GPS metadata')
        map_panel.grid(row=1, column=1, sticky=NSEW,  padx = 30, pady=30)

    root.title("Image metadata")
    root.mainloop()