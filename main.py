import customtkinter as ctk
import yfinance as yf
import pandas as pd
import numpy as np


APP_GEOMETRY = "400x150"
APP_TITLE = "Paper Trading"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry(APP_GEOMETRY)
        self.title(APP_TITLE)
        self.show_accueil()
        self.stocks = {
            "TSLA" : yf.download("TSLA", start="2024-01-01", end="2025-10-11", interval="1d"),
            "AAPL" : yf.download("AAPL", start="2024-01-01", end="2025-10-11", interval="1d"),
            "NVDA" : yf.download("NVDA", start="2024-01-01", end="2025-10-11", interval="1d")
        }
    
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()