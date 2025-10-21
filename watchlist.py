import customtkinter as ctk
from info import Info
from graphe import Graph

class Watchlist(ctk.CTkFrame):
    def __init__(self, master=None, stocks=None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.master.grid_rowconfigure(0, weight= 1)
        self.master.grid_columnconfigure(0, weight= 1)

        self.titre_label = ctk.CTkLabel(self, text="Watchlist", font=("Arial", 30, "bold"))
        self.titre_label.grid(row=0, column=0, pady=(10,10))
        
        i = 1

        for stock in self.stocks:
            self.titre_action = ctk.CTkButton(self, text=stock,fg_color = "transparent", hover_color="lightpink", font=("Arial", 24, "bold"), command=lambda s=stock: self.onButtonClicked(s))
            self.titre_action.grid(row=i, column=0, pady=(10,10))

            self.titre_prix_action = ctk.CTkButton(self, text=round(self.stocks[stock]['Close'].iloc[0].iloc[0], 2), fg_color = "transparent", hover_color="lightpink", font=("Arial", 24, "bold"), command=lambda s=stock: self.onButtonClicked(s))
            self.titre_prix_action.grid(row=i, column=1, pady=(10,10))

            self.boutonGraphe = ctk.CTkButton(self, text="Graphique", fg_color="transparent", hover_color="orange", font=("Arial", 24), command = lambda s = stock: self.on_button_click(s))
            self.boutonGraphe.grid(row=i, column=2, pady=(10,10))
            i += 1

    def clear_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        
    def onButtonClicked(self, pseudo):
        self.clear_main_frame()
        self.info = Info(self.master, self.stocks, pseudo)

    def on_button_click(self, name):
        self.clear_main_frame()
        self.graph = Graph(self.master, self.stocks, name)
