from customtkinter import CTkToplevel, CTkFrame, CTkLabel, set_appearance_mode, BOTH, LEFT, NSEW, NW, CENTER
from platform import system
import tkintermapview as tkmap

class Window(CTkToplevel):
    def __init__(self, n_panel, title):
        self.colors = ["#1C1C1C" , "#282828"]
        set_appearance_mode("dark")
        
        self.root = CTkToplevel()
        self.root.title(title)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{screen_width}x{screen_height}+0+0')
        if system() == "Linux":self.root.attributes('-zoomed', True)
        else : self.root.state("zoomed")
        self.root.attributes('-topmost', True)
        
        self.frame = CTkFrame(self.root, fg_color=self.colors[0])
        self.frame.pack(fill=BOTH, expand=True)
        self.frame.grid_rowconfigure([0,1], weight=1, uniform="row")
        self.frame.grid_columnconfigure([0,1], weight=1, uniform='col')
        
        def create_data_panel():
            self.data_panel = CTkLabel(self.frame, bg_color=self.colors[1], anchor=NW, justify=LEFT, padx=20, pady=20)
            self.data_panel.grid(column=0, rowspan=2, sticky=NSEW, padx = 30, pady=30)
            self.data_panel.update()
            self.data_panel.configure(wraplength = self.data_panel.winfo_width()-100)
        
        def create_preview_panel(span):
            create_data_panel()
            self.preview_panel = CTkLabel(self.frame, bg_color=self.colors[1], text='')
            self.preview_panel.grid(row=0, column=1, rowspan=span, sticky=NSEW,  padx = 30, pady=30)
    
        match n_panel :
            case 1 :
                create_data_panel()
            case 2: 
                create_preview_panel(span=2)
            case 3 : 
                create_preview_panel(span=1)        
                
    def create_map_panel(self, metadatas):
        try :
            map_panel = tkmap.TkinterMapView(self.frame)
            map_panel.set_position(deg_x=metadatas["Coordinates"][0], deg_y=metadatas["Coordinates"][1], marker=True)
            map_panel.grid(row=1, column=1, sticky=NSEW,  padx = 30, pady=30)
        except :
            map_panel = CTkLabel(self.frame, bg_color=self.colors[1], text='Map is unavailable :\nThere is no GPS metadata')
            map_panel.grid(row=1, column=1, sticky=NSEW,  padx = 30, pady=30)