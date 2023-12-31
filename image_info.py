from metadata_window import Window
from customtkinter import CTkImage, CENTER
from PIL import Image
from metadata_functions import get_image_metadata as exif

def fit(img, panel):
    """Find the best size to fit the best as possible an image into the preview panel, keeping the image aspect ratio
    Args:
        img (PIL Image): The image to fit into the panel
        panel (CTkLabel): The panel
    Returns:
        Tuple: The size (width, height) of the image to fit it in the panel
    """    
    img_size = img.size
    panel_size = (panel.winfo_width(), panel.winfo_height())
    img_ratio = img_size[0]/img_size[1]
    panel_ratio = panel_size[0]/panel_size[1]
    
    if img_ratio <= panel_ratio :
        return (panel_size[1]*img_ratio, panel_size[1])
    else :
        return (panel_size[0], panel_size[0]//img_ratio)
    
def metadata_parser(metadatas):
    """Parse the metadatas from a dictionnary to a text to display on the page
    Args:
        metadatas (dict): Dictionnairy containing the metadatas
    Returns:
        str: Pretty printing of the metadatas
    """
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
    """Create the window displaying the metadatas
    Args:
        file (str): The path to the file to analyse
    """
    
    img = Image.open(file)
    metadatas = exif(file)
    txt = metadata_parser(metadatas)
    
    # Create the window with 3 panels : Data, Preview and Map
    win = Window(n_panel=3, title="Image metadatas")
    
    win.data_panel.configure(state='normal')
    win.data_panel.insert('1.0', txt)
    win.data_panel.configure(state='disabled')
    
    # Place the image into the panel as a preview
    win.preview_panel.update()
    size = fit(img, win.preview_panel)
    img = CTkImage(light_image=img, dark_image=img, size=size)
    win.preview_panel.configure(image=img, anchor=CENTER, padx=0, pady=0)    
    
    # Create the map panel if there is GPS infos in the metadatas
    win.create_map_panel(metadatas=metadatas)

    win.root.mainloop()