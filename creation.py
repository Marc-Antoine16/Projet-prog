import customtkinter as ctk

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

        self.nom = ctk.CTkLabel(self, text="Entrer le nom du Compte: ", font=("Arial", 20))
        self.nom.grid(row=0, column=0, pady=(10,10))

        self.montant = ctk.CTkLabel(self, text="Entrer le montant à investir: ",  font=("Arial", 20))
        self.montant.grid(row=1, column=0, pady=(10,10))

        self.creation = ctk.CTkButton(self, text= "Créer le compte", font= ("Arial", 24))
        self.creation.grid(row=2, column=0, pady=(10,10))
