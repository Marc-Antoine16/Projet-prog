import customtkinter as ctk
from info import Info
import yfinance as yf
from graphe import Graph
import pandas as pd
import time

class Watchlist(ctk.CTkFrame):
    def __init__(self, master=None, stocks=None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        # importer la liste des stocks dans le S&P 500
        self.options = pd.read_csv("https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv")["Symbol"].tolist()
        self.options_with_placeholder = ["Ajouter..."] + self.options
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.master.grid_rowconfigure(0, weight= 1)
        self.master.grid_columnconfigure(0, weight= 1)

        self.titre_label = ctk.CTkLabel(self, text="Watchlist", font=("Arial", 30, "bold"))
        self.titre_label.grid(row=0, column=0, pady=(10,10))

        self.dropdown = ctk.CTkOptionMenu(self,values=self.options_with_placeholder, command=self.option_changed)
        self.dropdown.set("Ajouter...")
        self.dropdown.grid(row=0, column=4, pady=(10,10))
        
        i = 1

        i = 1
        for stock in self.stocks:
            self.titre_action = ctk.CTkButton(self, text=stock,fg_color = "transparent", hover_color="lightpink", font=("Arial", 24, "bold"), command=lambda s=stock: self.onButtonClicked(s))
            self.titre_action.grid(row=i, column=0, pady=(10,10))

            self.boutonGraphe = ctk.CTkButton(self, text="Graphique", fg_color="transparent", hover_color="orange", font=("Arial", 24), command = lambda s = stock: self.on_button_click(s))
            self.boutonGraphe.grid(row=i, column=2, pady=(10,10))
            
            self.bouton_supprime = ctk.CTkButton(self, text="Supprimer", fg_color="transparent", hover_color="red", font=("Arial", 24), command = lambda s = stock: self.supprime_stock(s))
            self.bouton_supprime.grid(row=i, column=3, pady=(10,10))

            i += 1      

        self.boucle_stock(1)

    def boucle_stock(self, temps):
        if temps == len(self.stocks[next(iter(self.stocks))]['Close']):
            temps = 1
        
        else:
            for widget in self.winfo_children():
                    info = widget.grid_info()
                    col = info.get("column")
                    row = info.get("row")
                    if (col == 1 and row != 0) or (col == 3 and row == 0):
                        widget.destroy()

            i = 1
            for stock in self.stocks:
                self.titre_prix_action = ctk.CTkButton(self, text=round(self.stocks[stock]['Close'].iloc[temps].iloc[0], 2), fg_color = "transparent", hover_color="lightpink", font=("Arial", 24, "bold"), command=lambda s=stock: self.onButtonClicked(s))
                self.titre_prix_action.grid(row=i, column=1, pady=(10,10))

                i += 1   

            self.date = ctk.CTkLabel(self, text=self.stocks[stock]. index[temps].date(), text_color= "light gray", font=("Arial", 24))
            self.date.grid(row=0, column=3, padx = (0, 10), pady=(10,10))
            
            self.boucle_id = self.after(5000, lambda: self.boucle_stock(temps + 1))

    def clear_main_frame(self):
        if hasattr(self, "boucle_id"):
            self.after_cancel(self.boucle_id)
            
        for widget in self.winfo_children():
            widget.destroy()
        self.dropdown.destroy()
        
        
    def onButtonClicked(self, pseudo):
        self.clear_main_frame()
        Info(self.master, self.stocks, pseudo)

    def on_button_click(self, name):
        self.clear_main_frame()
        Graph(self.master, self.stocks, name)
    
    def supprime_stock(self, nom):
        del self.stocks[nom]
        self.clear_main_frame()
        self.create_widgets()

    def option_changed(self, value):
        if value == "Ajouter...":
            return
        self.current_choice = value
        self.stocks[value] = yf.download(value, start="2024-01-01", end="2025-10-11", interval="1d")
        self.clear_main_frame()
        self.create_widgets()
