from customtkinter import *
from PIL import Image
from metadata_functions import get_pdf_metadata as pdf
from pdf2image import convert_from_path
from platform import system

#convert_from_path()

colors = ["#1C1C1C" , "#282828"]

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
    
    root = CTkToplevel()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f'{screen_width}x{screen_height}+0+0')
    if system() == "Linux":root.attributes('-zoomed', True)
    else : root.state("zoomed")
    
    frame = CTkFrame(root, fg_color=colors[0])
    frame.pack(fill=BOTH, expand=True)
    frame.grid_rowconfigure([0,1], weight=1, uniform="row")
    frame.grid_columnconfigure([0,1], weight=1, uniform='col')
        
    data_panel = CTkLabel(frame, bg_color=colors[1], text=txt, anchor=NW, justify=LEFT, padx=20, pady=20)
    data_panel.grid(column=0, rowspan=2, sticky=NSEW, padx = 30, pady=30)
    data_panel.update()
    data_panel.configure(wraplength = data_panel.winfo_width()-100)
    
    if txt == "There is no metadata in this file.\nTry another one." :
        data_panel.configure(justify=CENTER, anchor=CENTER)

    root.title("PDF metadata")
    root.mainloop()