import customtkinter as ctk
import yfinance as yf
import pandas as pd
import numpy as np
from watchlist import Watchlist


APP_GEOMETRY = "800x600"
APP_TITLE = "Paper Trading"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(APP_GEOMETRY)
        self.title(APP_TITLE)
        self.stocks = {
            "TSLA" : yf.download("TSLA", start="2024-01-01", end="2025-10-11", interval="1d"),
            "AAPL" : yf.download("AAPL", start="2024-01-01", end="2025-10-11", interval="1d"),
            "NVDA" : yf.download("NVDA", start="2024-01-01", end="2025-10-11", interval="1d")
        }
        print(self.stocks["TSLA"].head())
        self.show_watchlist()

    def show_watchlist(self):
        self.watchlist = Watchlist(master=self,stocks=self.stocks)
    
if __name__ == "__main__":
    app = MainApp() 
    app.mainloop()