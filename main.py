import customtkinter as ctk
import yfinance as yf
import pandas as pd
import numpy as np
from watchlist import Watchlist
from graphe import GraphPage



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
        
        self.current_page = None
        self.show_watchlist()


    def clear_page(self):
        if self.current_page is not None:
            self.current_page.destroy()

    def show_graph(self):
        self.clear_page()
        self.current_page = GraphPage(master = self, stocks=self.stocks)

    
    def show_watchlist(self):
        self.clear_page()
        self.current_page = Watchlist(master=self,stocks=self.stocks, go_to_graph=self.show_graph)
    
if __name__ == "__main__":
    app = MainApp() 
    app.mainloop()