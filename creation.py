import customtkinter as ctk
import json
import os


class Creation(ctk.CTkFrame):
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

        self.btn_nom = ctk.CTkLabel(self, text="Entrer le nom du Compte: ", font=("Arial", 20))
        self.btn_nom.grid(row=2, column=2, pady=(10,10))

        self.btn_montant = ctk.CTkLabel(self, text="Entrer le montant à investir ($) : ",  font=("Arial", 20))
        self.btn_montant.grid(row=3, column=2, pady=(10,10))

        self.btn_creation = ctk.CTkButton(self, text= "Créer le compte", font= ("Arial", 24), command=self.creer_compte)
        self.btn_creation.grid(row=4, column=3, pady=(10,10))

        self.btn_retour = ctk.CTkButton(self, text="Retour",fg_color="transparent",hover_color="light green",font=("Arial", 24, "bold"),command=self.aller_A_accueil)
        self.btn_retour.grid(row=0, column=0, pady=(0, 0))

        self.entre_nom= ctk.CTkEntry(self, width=200, font=("Arial", 18))
        self.entre_nom.grid(row=2,column=3, pady=(10,10))

        self.entre_montant= ctk.CTkEntry(self, width=200, font=("Arial", 18))
        self.entre_montant.grid(row=3,column=3, pady=(10,10))

    def creer_compte(self):
        nom=self.entre_nom.get()
        montant= self.entre_montant.get()

        try:
            montant = float(montant)
        except ValueError:
            self.erreurMontant = ctk.CTkLabel(self, text="Enter un nombre valide", font=("Arial", 18), text_color="red")
            self.erreurMontant.grid(row=1 , column= 1, pady=(10,10))
            return
        
        compte={"nom" : nom , "montant": montant }
        if os.path.exists("comptes.json"):
            with open("comptes.json", "r") as f:
                data = json.load(f)
        else:
            data=[]

        data.append(compte)

        with open("comptes.json", "w") as f:
            json.dump(data,f,indent=4)

        msgAide=ctk.CTkLabel(self, text=f"Compte créé ! Appuyer sur votre compte ({nom}) pour commencer à négocier.", text_color="red", font=("Arial", 16))
        msgAide.grid(row=4,column = 3, pady=(10,10))
        
        self.clear_main_frame()
        self.show_accueil()
        
    
    def aller_A_accueil(self):
        self.show_accueil()
        
    def show_accueil(self):
        from accueil import Accueil
        self.clear_main_frame()
        self.destroy()
        self.current_page = Accueil(master=self.master) #Parent
        self.current_page.grid(row=0, column=0, sticky="nsew")
        

    def clear_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
    
