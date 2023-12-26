import customtkinter as ctk
import main_page

dossier = ""

def choisir_dossier():
    dossier = ctk.filedialog.askdirectory()
    if dossier:
        root.destroy()
        main_page.main(dossier)

# Créer la fenêtre principale
root = ctk.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.title("Page d'accueil")

# Créer et placer les widgets
label_instructions = ctk.CTkLabel(root, text="Choisissez un dossier local :", font=('',20))
label_instructions.pack(pady=10)

button_choisir = ctk.CTkButton(root, text="Choisir un dossier", command=choisir_dossier, font=('',20))
button_choisir.pack(pady=20)

# Lancer l'application
root.eval('tk::PlaceWindow . center')
root.mainloop()