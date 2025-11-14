import customtkinter as ctk
import yfinance as yf
import pandas as pd
import numpy as np
from watchlist import Watchlist
from graphe import Graph
from login import LoginPage
from datetime import date
from menu import MenuBar



APP_GEOMETRY = "900x700"
APP_TITLE = "Paper Trading"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")      
        self.geometry(APP_GEOMETRY)
        self.title(APP_TITLE)
        self.date = date.today()
        self.stocks = {
            "TSLA" : yf.download("TSLA", start="2024-01-01", end=f"{self.date}", interval="1d"),
            "AAPL" : yf.download("AAPL", start="2024-01-01", end=f"{self.date}", interval="1d"),
            "NVDA" : yf.download("NVDA", start="2024-01-01", end=f"{self.date}", interval="1d"),
            "MSFT" : yf.download("MSFT", start="2024-01-01", end=f"{self.date}", interval="1d")
        }
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.update_menu(self.stocks, 1, None)
        self.show_watchlist()

    def update_menu(self, stocks, temps, compte):
        self.menu = MenuBar(master=self, stocks=stocks, temps=temps, compte=compte)
    
    def clear_main_frame(self):
        if hasattr(self, "boucle_id"):
            try:
                self.after_cancel(self.boucle_id)
            except Exception:
                pass

        for widget in self.winfo_children():
            widget.destroy()

    def show_watchlist(self):
        self.current_page = Watchlist(master=self,stocks=self.stocks, temps= 1)

    def show_login(self):
        self.current_page = LoginPage(master=self, stocks=self.stocks)
    
if __name__ == "__main__":
    app = MainApp() 
    app.mainloop()