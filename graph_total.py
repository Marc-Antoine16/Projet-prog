import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import json
import os
import time

class GraphTotal(ctk.CTkFrame):

    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.data_x = []
        self.data_y = []

        self.create_widgets()
        self.update_graph()

    def create_widgets(self):

        self.grid(row=0, column=0, sticky="nsew")

        self.fig, self.ax = plt.subplots(figsize=(9,5))
        self.fig.patch.set_facecolor("black")
        self.ax.set_facecolor("black")

        for spine in self.ax.spines.values():
            spine.set_color("white")

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.title.set_color('white')
        self.ax.yaxis.label.set_color('white')

        self.ax.set_title("Rendement total du portefeuille")
        self.ax.set_ylabel("Rendement (%)")


        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=20)

        btn_retour = ctk.CTkButton(self, text="← Retour", fg_color="transparent",hover_color="green", font=("Arial", 20),command=self.retour_accueil)
        btn_retour.grid(row=0, column=0, pady=(10, 10))

    def calcul_rendement_total(self):
        if not os.path.exists("comptes.json"):
            return 0

        with open("comptes.json", "r") as f:
            comptes = json.load(f)

        total_investi = 0
        total_valeur = 0

        for compte in comptes:
            for symbole, info in compte["actions"].items():
                quantite = info["quantite"]
                prix_achat = info["prix_achat"]

                if quantite <= 0:
                    continue

                try:
                    prix_actuel = yf.Ticker(symbole).history(period="1d")["Close"].iloc[-1]
                except:
                    continue

                total_investi += prix_achat * quantite
                total_valeur += prix_actuel * quantite

        if total_investi == 0:
            return 0

        rendement = ((total_valeur - total_investi) / total_investi) * 100
        return rendement

    def update_graph(self):
        self.data_x.append(time.strftime("%H:%M:%S"))
        self.data_y.append(self.calcul_rendement_total())

        self.ax.clear()
        self.ax.plot(self.data_x, self.data_y, linewidth=2)
        self.ax.set_title("Rendement total du portefeuille")
        self.ax.set_ylabel("Rendement (%)")

        self.ax.tick_params(axis='x', colors='white', rotation=45)
        self.ax.tick_params(axis='y', colors='white')

        for spine in self.ax.spines.values():
            spine.set_color("white")

        self.ax.set_facecolor("black")

        self.canvas.draw()

        self.after(5000, self.update_graph)

    def retour_accueil(self):
        from accueil import Accueil
        self.destroy()
        self.master.current_page = Accueil(master=self.master)
        self.master.current_page.grid(row=0, column=0, sticky="nsew")
