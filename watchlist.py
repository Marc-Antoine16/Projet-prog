import customtkinter as ctk
from info import Info
import yfinance as yf
from graphe import Graph
import pandas as pd

class Watchlist(ctk.CTkFrame):
    def __init__(self, master=None, stocks=None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        # importer la liste des stocks dans le S&P 500
        self.options = pd.read_csv("https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv")["Symbol"].tolist()
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.master.grid_rowconfigure(0, weight= 1)
        self.master.grid_columnconfigure(0, weight= 1)

        self.titre_label = ctk.CTkLabel(self, text="Watchlist", font=("Arial", 30, "bold"))
        self.titre_label.grid(row=0, column=0, pady=(10,10))

        self.dropdown = ctk.CTkOptionMenu(master=self.master, values=self.options, command=self.option_changed)
        self.dropdown.grid(row=0, column=3, pady=(10,10))
        
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
        self.dropdown.destroy()
        
    def onButtonClicked(self, pseudo):
        self.clear_main_frame()
        self.info = Info(self.master, self.stocks, pseudo)

    def on_button_click(self, name):
        self.clear_main_frame()
        self.graph = Graph(self.master, self.stocks, name)

    def option_changed(self, value):
        self.current_choice = value
        self.stocks[value] = yf.download(value, start="2024-01-01", end="2025-10-11", interval="1d")
        self.clear_main_frame()
        self.create_widgets()