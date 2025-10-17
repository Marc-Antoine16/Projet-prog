import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphPage(ctk.CTkFrame):
    def __init__(self, master=None, stocks = None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.create_widgets()

    def create_widgets(self):
            
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.titre_label = ctk.CTkLabel(self, text="Watchlist", font=("Arial", 30, "bold"))
        self.titre_label.grid(row=0, column=0, pady=(10,10))
        self.titre_action = ctk.CTkLabel(self, text="TSLA", font=("Arial", 24, "bold"))
        self.titre_action.grid(row=1, column=0, pady=(10,10))
        self.titre_prix_action = ctk.CTkLabel(self, text=self.stocks["TSLA"].iloc[2]['Close'], font=("Arial", 24, "bold"))
        self.titre_prix_action.grid(row=1, column=1, pady=(10,10))
        self.boutonGraphe = ctk.CTkButton(self, text="Graphique", fg_color="#1E90FF")
        self.boutonGraphe.grid(row=1, column=2, pady=(10,10), command = self.on_button_click)
