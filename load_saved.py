from customtkinter import *
from platform import system
from metadata_functions import load_and_print
from json import dumps

def read(file):

        colors = ["#1C1C1C" , "#282828"]
        set_appearance_mode("dark")
        root = CTk()
        root.title("Main page")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f'{screen_width}x{screen_height}+0+0')
        if system() == "Linux":root.attributes('-zoomed', True)
        else : root.state("zoomed")
        
        canvas = CTkCanvas(root, bg=colors[0], highlightthickness=0)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = CTkScrollbar(root, orientation=VERTICAL, command=canvas.yview, corner_radius=0)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        frame = CTkFrame(canvas, fg_color=colors[0])
        root.update()
        canvas.create_window((root.winfo_width()//2, 0), window=frame, anchor=N, width=root.winfo_width())
            
        data = dumps(load_and_print(file), indent=2)
        
        label = CTkLabel(frame, text=data, anchor=NW)
        label.pack(fill=X, padx=100)
        
        canvas.update()
        w = canvas.winfo_width()-200
        label.configure(wraplength=w, justify=LEFT)

        text_height = label.winfo_reqheight()
        canvas.configure(scrollregion=(0, 0, 0, text_height))

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        label.bind("<Configure>", on_frame_configure)
        root.mainloop()

def main():
    
    file = filedialog.askopenfile(filetypes=[("JSON files", "*.json")])
    if file:
        read(file.name)   
