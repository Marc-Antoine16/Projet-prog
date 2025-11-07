import customtkinter as ctk
from titreDetenues import TitreDetenues
from placement import Placement
from creation import Creation

class Accueil(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.create_widgets()
    
    def create_widgets(self):

        self.master.grid_rowconfigure(0, weight= 1)
        self.master.grid_columnconfigure(0, weight= 1)

        # Le frame a plusieurs colonnes extensibles
        self.grid_rowconfigure((0, 1, 2,4,5,6,7,8,9,10), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5,6,7,8,9,10), weight=1)

        self.titre_label = ctk.CTkLabel(self, text="Accueil", font=("Arial", 32, "bold"))
        self.titre_label.grid(row=0, column=5, pady=(10,10))

        self.bouton_solde = ctk.CTkButton(self, text=f"solde ... $", font=("Arial", 20), command= self.ouvrir_placement)
        self.bouton_solde.grid(row=1, column=5, pady=(10,10))

        self.bouton_titres = ctk.CTkButton(self, text= "Titres detenues ->", font=("Arial", 20), command= self.ouvrir_titreDetenues)
        self.bouton_titres.grid(row=3, column=5, pady=(10,10))

        self.compte_label = ctk.CTkLabel(self, text = "Compte(s)", font=("Arial", 24))
        self.compte_label.grid(row=5, column= 1, pady=(10,10))

        self.bouton_compte = ctk.CTkButton(self, text = "Créer un compte", fg_color="transparent", hover_color="red", font=("Arial", 20), command =self.creer_compte)
        self.bouton_compte.grid(row = 6, column = 1, pady = (10,10))

    def ouvrir_titreDetenues(self):
        self.clear_main_frame()
        TitreDetenues(self.master)

    def ouvrir_placement(self):
        self.clear_main_frame()
        Placement(self.master)
    
    def creer_compte(self):
        self.clear_main_frame()
        Creation(self.master)

    def clear_main_frame(self):
            if hasattr(self, "boucle_id"):
                try:
                    self.after_cancel(self.boucle_id)
                except Exception:
                    pass

            for widget in self.winfo_children():
                widget.destroy()
    

        