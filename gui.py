import tkinter as tk
import customtkinter as ctk


def choisir_dossier():
    dossier = ctk.filedialog.askdirectory()
    if dossier:
        label_dossier.configure(text=f"Dossier choisi : {dossier}")

# Créer la fenêtre principale
root = ctk.CTk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}+0+0")
root.title("Page d'accueil")

# Créer et placer les widgets
label_instructions = ctk.CTkLabel(root, text="Choisissez un dossier local :")
label_instructions.pack(pady=10)

button_choisir = ctk.CTkButton(root, text="Choisir un dossier", command=choisir_dossier)
button_choisir.pack(pady=10)

label_dossier = ctk.CTkLabel(root, text="Dossier choisi :")
label_dossier.pack(pady=10)

# Lancer l'application
root.mainloop()