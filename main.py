import customtkinter as ctk
import yfinance as yf
import pandas as pd
import numpy as np
from watchlist import Watchlist
from graphe import Graph
from accueil import Accueil


APP_GEOMETRY = "900x600"
APP_TITLE = "Paper Trading"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")      
        self.geometry(APP_GEOMETRY)
        self.title(APP_TITLE)
        self.protocol("WM_DELETE_WINDOW", self.quit)
        #self.show_watchlist()
        self.show_accueil()

    def show_accueil(self):
        self.current_page = Accueil(master=self)
        self.current_page.grid(row=0, column=0, sticky="nsew") #nsew: le widget s’aligne au centre de la cellule et s’étire avec la fenêtre.

    def show_watchlist(self):
        self.current_page = Watchlist(master=self,stocks=self.stocks, temps= 1)
    
    def switch_frame(self, frame_class, **kwargs):
        #Détruit la page actuelle et affiche la nouvelle
        if self.current_page is not None:
            self.current_page.destroy()

        self.current_page = frame_class(master=self, **kwargs)
        self.current_page.grid(row=0, column=0, sticky="nsew")
    
if __name__ == "__main__":
    app = MainApp() 
    app.mainloop()