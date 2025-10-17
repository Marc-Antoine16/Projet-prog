import customtkinter as ctk

class Watchlist(ctk.CTkFrame):
    def __init__(self, master=None, stocks=None, go_to_graph = None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.go_to_graph = go_to_graph
        self.create_widgets()



    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.titre_label = ctk.CTkLabel(self, text="Watchlist", font=("Arial", 30, "bold"))
        self.titre_label.grid(row=0, column=0, pady=(10,10))
        self.titre_action = ctk.CTkLabel(self, text="TSLA", font=("Arial", 24, "bold"))
        self.titre_action.grid(row=1, column=0, pady=(10,10))
        self.titre_prix_action = ctk.CTkLabel(self, text=self.stocks["TSLA"].iloc[2]['Close'], font=("Arial", 24, "bold"))
        self.titre_prix_action.grid(row=1, column=1, pady=(10,10))
        self.boutonGraphe = ctk.CTkButton(self, text="Graphique", fg_color="#1E90FF", command = self.on_button_click)
        self.boutonGraphe.grid(row=1, column=2, pady=(10,10))

    def on_button_click(self):
        if self.go_to_graph:
            self.go_to_graph()
        
# class Accueil(ctk.CTkFrame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.create_widgets()
#         self.protocol("WM_DELETE_WINDOW" ,self.quit) #fermer l'application proprement quand on clique sur lacroix
#     def create_widgets(self):
#         self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew") # Grille
#         self.button = ctk.CTkButton(self, text="my button", command=self.button_callback) 
#         self.button.grid(row=0, column=0, pady=(20,10))
#         # Bouton
#         self.label = ctk.CTkLabel(self, text="CTkLabel", fg_color="transparent")# Label
#         self.label.grid(row=1, column=0, pady=(10,10))
#     def button_callback(self):
#         print("button clicked")
#         self.label.configure(text="Vous avez cliqué sur le bouton")