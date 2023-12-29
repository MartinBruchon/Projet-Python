from customtkinter import *
from PIL import Image
from metadata_functions import get_pdf_metadata as pdf
from platform import system
from pdf2jpg import pdf2jpg
import shutil

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
    try :
        for e in metadatas["Full"] :
            txt += str(e)[1:]+" : "+str(metadatas["Full"][e])+"\n"
    except :
        txt = "There is no metadata in this file.\nTry another one."
    return txt

def main(file):
    
    set_appearance_mode("dark")
    
    metadatas = pdf(file)
    txt = metadata_parser(metadatas)
    
    try :
        res = pdf2jpg.convert_pdf2jpg(file, ".", pages="0")
        dir, f = res[0]["output_pdfpath"], res[0]["output_jpgfiles"][0]
        img = Image.open(f)
        shutil.rmtree(dir)
        preview_available = True
    except :
        preview_available = False
        
    root = CTkToplevel()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    #root.geometry(f'{screen_width}x{screen_height}+0+0')
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
    
    if preview_available == True :
        preview_panel.update()
        size = fit(img, preview_panel)
        img = CTkImage(light_image=img, dark_image=img, size=size)
        preview_panel.configure(image=img, anchor=CENTER, padx=0, pady=0)    
    else :
        preview_panel.configure(text="You need JAVA to be installed\nto see a preview", anchor=CENTER, padx=0, pady=0)
    
    if txt == "There is no metadata in this file.\nTry another one." :
        data_panel.configure(justify=CENTER, anchor=CENTER)

    root.title("PDF metadata")
    root.mainloop()