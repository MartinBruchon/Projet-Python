from customtkinter import CTkToplevel, CTkFrame, CTkLabel, set_appearance_mode, BOTH, LEFT, NSEW, NW, CENTER
from platform import system
import tkintermapview as tkmap
from tkinter import Text 

class Window(CTkToplevel):
    """Creation of a new class heriting of customtkinter.CTkToplevel to easily create new windows for metadata displaying
    Args:
        CTkToplevel (CTkToplevel): Window based on customtkinter.CTkToplevel
    """    
    def __init__(self, n_panel, title):
        """Creation of the base window and settings of the common parameters
        Args:
            n_panel (int): The number of visualisation panel from 1 to 3 : for data, preview image or map 
            title (str): The title of the window
        """     
        
        # Base settings initialization   
        self.colors = ["#1C1C1C" , "#282828"]
        set_appearance_mode("dark")
        
        # Creation of the window
        self.root = CTkToplevel()
        self.root.title(title)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{screen_width}x{screen_height}+0+0')
        if system() == "Linux":self.root.attributes('-zoomed', True)
        else : self.root.state("zoomed")
        self.root.attributes('-topmost', True)
        
        # Creation of the frame which will contains the different panels
        self.frame = CTkFrame(self.root, fg_color=self.colors[0])
        self.frame.pack(fill=BOTH, expand=True)
        self.frame.grid_rowconfigure([0,1], weight=1, uniform="row")
        self.frame.grid_columnconfigure([0,1], weight=1, uniform='col')
        
        def create_data_panel():
            """Creation of the data panel, to the left of the window
            """            
            self.data_panel = Text(self.frame, wrap="word", bg=self.colors[1], fg='white', borderwidth=-1, state='disabled', padx=20, pady=20)
            self.data_panel.grid(column=0, rowspan=2, sticky=NSEW, padx = 30, pady=30)
            self.data_panel.update()
        
        def create_preview_panel(span):
            """Creation of the preview panel at the right or the top right depending of the total number of panel in the window
            Args:
                span (int): Rowspan number for the grid layout to allow to place a third panel at the bottom right if needed
            """            
            create_data_panel()
            self.preview_panel = CTkLabel(self.frame, bg_color=self.colors[1], text='')
            self.preview_panel.grid(row=0, column=1, rowspan=span, sticky=NSEW,  padx = 30, pady=30)
    
        # Creation of the different requested panels
        match n_panel :
            case 1 :
                create_data_panel()
            case 2: 
                create_preview_panel(span=2)
            case 3 : 
                create_preview_panel(span=1)        
                
    def create_map_panel(self, metadatas):
        """Method of the class allowing to create the map view panel according to the extracted metadatas
        Args:
            metadatas (dict): Dictionnary of all the metadatas of the image
        """        
        try :
            # Try to create the map
            map_panel = tkmap.TkinterMapView(self.frame)
            map_panel.set_position(deg_x=metadatas["Coordinates"][0], deg_y=metadatas["Coordinates"][1], marker=True)
            map_panel.grid(row=1, column=1, sticky=NSEW,  padx = 30, pady=30)
        except :
            # If there is no GPS metadata, replace the mapview by a label
            map_panel = CTkLabel(self.frame, bg_color=self.colors[1], text='Map is unavailable :\nThere is no GPS metadata')
            map_panel.grid(row=1, column=1, sticky=NSEW,  padx = 30, pady=30)