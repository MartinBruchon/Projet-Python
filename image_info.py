from metadata_window import Window
from customtkinter import CTkImage, CENTER
from PIL import Image
from metadata_functions import get_image_metadata as exif

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
    if metadatas != {}:
        for e in metadatas["Full"] :
            txt += str(e)+" : "+str(metadatas["Full"][e])+"\n"
        for e in metadatas :
            if e != "Full" : txt += str(e)+" : "+str(metadatas[e])+"\n"
    else :
        txt = "There is no metadata in this file.\nTry another one."
                
    return txt

def main(file):
    
    img = Image.open(file)
    metadatas = exif(file)
    txt = metadata_parser(metadatas)
    
    win = Window(n_panel=3, title="Image metadatas")
    
    win.data_panel.configure(state='normal')
    win.data_panel.insert('1.0', txt)
    win.data_panel.configure(state='disabled')
    
    win.preview_panel.update()
    size = fit(img, win.preview_panel)
    img = CTkImage(light_image=img, dark_image=img, size=size)
    win.preview_panel.configure(image=img, anchor=CENTER, padx=0, pady=0)    
    
    win.create_map_panel(metadatas=metadatas)

    win.root.mainloop()