import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class GraphPage(ctk.CTkFrame):
    def __init__(self, master=None, stocks = None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.create_widgets()

    def create_widgets(self):
        df = self.stocks["TSLA"]
        x = df.index
        y=df["Close"]
        plt.figure(figsize=(5,4))
        plt.plot(x,y, label = "Prix en fonction de la journée")
        plt.xlabel("Date")
        plt.ylabel("Prix")
        plt.show()
            
        
