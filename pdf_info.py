from metadata_window import Window
from customtkinter import CTkImage, CENTER
from PIL import Image
from metadata_functions import get_pdf_metadata as pdf
from pdf2jpg import pdf2jpg
import shutil

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
    try :
        for e in metadatas :
            txt += str(e)+" : "+str(metadatas[e])+"\n"
    except :
        txt = "There is no metadata in this file.\nTry another one."
    return txt

def main(file):
    """Create the window displaying the metadatas
    Args:
        file (str): The path to the file to analyse
    """
        
    metadatas = pdf(file)
    txt = metadata_parser(metadatas)
    
    # Try on convert the first page of the PDF file to JPG image to load it as preview
    try :
        res = pdf2jpg.convert_pdf2jpg(file, ".", pages="0")
        dir, f = res[0]["output_pdfpath"], res[0]["output_jpgfiles"][0]
        img = Image.open(f)
        preview_available = True
    except :
        preview_available = False
        
    # Create the window with 2 panels for the data and the preview
    win = Window(n_panel=2, title="PDF metadatas")
    
    # If the extraction of the first page succeed, display it in the app and remove the temporary image of the filesystem
    if preview_available == True :
        win.preview_panel.update()
        size = fit(img, win.preview_panel)
        img = CTkImage(light_image=img, dark_image=img, size=size)
        win.preview_panel.configure(image=img, anchor=CENTER, padx=0, pady=0)  
        try : shutil.rmtree(dir)  
        except : print("The folder cannot be deleted")
    else :
        win.preview_panel.configure(text="You need JAVA to be installed\nto see a preview", anchor=CENTER, padx=0, pady=0)
    
    win.data_panel.configure(state='normal')
    win.data_panel.insert('1.0', txt)
    win.data_panel.configure(state='disabled')

    win.root.mainloop()