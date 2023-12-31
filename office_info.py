from metadata_window import Window, CENTER
from metadata_functions import get_office_metadata as office

def metadata_parser(metadatas):
    txt = ""
    try :
        for e in metadatas :
            txt += str(e)+" : "+str(metadatas[e])+"\n"
    except :
        txt = "There is no metadata in this file.\nTry another one."
    return txt

def main(file):
    
    win = Window(n_panel=1, title="Office Document metadatas")
    
    metadatas = office(file)
    txt = metadata_parser(metadatas)    
    
    #win.data_panel.configure(text=txt)
    win.data_panel.configure(state='normal')
    win.data_panel.insert('1.0', txt)
    win.data_panel.configure(state='disabled')

    win.root.mainloop()