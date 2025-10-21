import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class Graph(ctk.CTkFrame):
    def __init__(self, master=None, stocks = None, nom = None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.nom = nom
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        self.master.grid_rowconfigure(0, weight= 1)
        self.master.grid_columnconfigure(0, weight= 1)

        x = self.stocks[self.nom].index
        y = self.stocks[self.nom]["Close"]

        plt.figure(figsize= (9,6))
        plt.plot (x, y, label = "Prix en fonction de la journée")
        plt.xlabel("Date")
        plt.ylabel("Prix")

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master = self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 1, column= 0, pady=(10, 10))

        self.watchlist_button = ctk.CTkButton(self, text="retour", fg_color = "transparent", hover_color= "light green", font=("Arial", 15, "bold"), command= self.retour)
        self.watchlist_button.grid(row=0, column=0, pady=(0,0))

    def clear_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def retour(self):
        from watchlist import Watchlist
        self.clear_main_frame()
        Watchlist(self.master, self.stocks)