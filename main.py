import customtkinter as ctk
import yfinance as yf
import pandas as pd
import numpy as np
from watchlist import Watchlist
from graphe import Graph



APP_GEOMETRY = "800x600"
APP_TITLE = "Paper Trading"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")      
        self.geometry(APP_GEOMETRY)
        self.title(APP_TITLE)
        self.stocks = {
            "TSLA" : yf.download("TSLA", start="2024-01-01", end="2025-10-11", interval="1d"),
            "AAPL" : yf.download("AAPL", start="2024-01-01", end="2025-10-11", interval="1d"),
            "NVDA" : yf.download("NVDA", start="2024-01-01", end="2025-10-11", interval="1d")
        }
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.show_watchlist()
    def show_watchlist(self):
        self.current_page = Watchlist(master=self,stocks=self.stocks, temps= 1)
    
if __name__ == "__main__":
    app = MainApp() 
    app.mainloop()