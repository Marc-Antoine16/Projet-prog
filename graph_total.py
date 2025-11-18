import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
import json
import os
from datetime import datetime
import pandas as pd   

class GraphTotal(ctk.CTkFrame):

    HISTORY_FILE = "historique_total.json"
    UPDATE_INTERVAL = 5000  

    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.data_x = []  
        self.data_y = []  
        self.current_period = "ALL"  # "ALL", "1J", "1S", "1M"

        self.load_history()      # Charge l'historique s'il existe
        self.create_widgets()    
        self.update_graph()      # Lance la mise à jour en boucle


    def create_widgets(self):

        self.grid(row=0, column=0, sticky="nsew")

        # Configuration de la grille
        self.grid_rowconfigure(0, weight=0)   # ligne boutons
        self.grid_rowconfigure(1, weight=1)   # ligne graph
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.fig, self.ax = plt.subplots(figsize=(9, 5))
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
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2,
                                         sticky="nsew", pady=20)

        #Bouton retour
        btn_retour = ctk.CTkButton(self,text="← Retour",fg_color="transparent",hover_color="green",font=("Arial", 20),command=self.retour_accueil)
        btn_retour.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        #Boutons de période
        frame_btn = ctk.CTkFrame(self, fg_color="transparent")
        frame_btn.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        frame_btn.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(frame_btn, text="1J",fg_color="transparent", hover_color="gray30",command=lambda: self.change_period("1J")).grid(row=0, column=0, padx=5)

        ctk.CTkButton(frame_btn, text="1S",fg_color="transparent", hover_color="gray30",command=lambda: self.change_period("1S")).grid(row=0, column=1, padx=5)

        ctk.CTkButton(frame_btn, text="1M",fg_color="transparent", hover_color="gray30",command=lambda: self.change_period("1M")).grid(row=0, column=2, padx=5)

        ctk.CTkButton(frame_btn, text="TOUT",fg_color="transparent", hover_color="gray30",command=lambda: self.change_period("ALL")).grid(row=0, column=3, padx=5)



    def load_history(self):
        #Charge l'historique du rendement total depuis le JSON, si dispo.

        if not os.path.exists(self.HISTORY_FILE):
            return

        try:
            with open(self.HISTORY_FILE, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return

        self.data_x = [item["timestamp"] for item in data]
        self.data_y = [item["rendement"] for item in data]

    def save_point(self, timestamp, rendement):
        #Ajoute un point de rendement dans le fichier d'historique.
        historique = []
        if os.path.exists(self.HISTORY_FILE):
            try:
                with open(self.HISTORY_FILE, "r") as f:
                    historique = json.load(f)
            except json.JSONDecodeError:
                historique = []

        historique.append({"timestamp": timestamp, "rendement": rendement})

        with open(self.HISTORY_FILE, "w") as f:
            json.dump(historique, f, indent=4)


    def calcul_rendement_total(self,index):
        if not os.path.exists("comptes.json"):
            return 0

        with open("comptes.json", "r") as f:
            try:
                comptes = json.load(f)
            except json.JSONDecodeError:
                return 0

        total_investi = 0
        total_valeur = 0

        for compte in comptes:
            actions = compte.get("actions,{}")
            for symbole, info in actions.items():
                quantite = info.get("quantite", 0)
                prix_achat = info.get("prix_achat", 0)

                if quantite <= 0 or prix_achat <= 0:
                    continue

                try:
                   df = yf.download(symbole, start="2024-01-01", interval="1d")
                   df["Close"] = df["Close"].astype(float)
                except Exception:
                    continue
                    
                 # Protection si index dépasse la longueur
                if index < len(df):
                    prix_actuel = float(df["Close"].iloc[index])
                else:
                    prix_actuel = float(df["Close"].iloc[-1])

                total_investi += prix_achat * quantite
                total_valeur += prix_actuel * quantite

        if total_investi == 0:
            return 0

        rendement = ((total_valeur - total_investi) / total_investi) * 100
        return float(rendement)

    def update_graph(self):
        #Ajoute un point, sauvegarde, et redessine selon la période.

        # Si le frame est détruit, on arrête
        if not self.winfo_exists():
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rendement = self.calcul_rendement_total()

        self.data_x.append(timestamp)
        self.data_y.append(rendement)
        self.save_point(timestamp, rendement)

        self.redraw_for_period()

        # replanifie l'update
        self.after(self.UPDATE_INTERVAL, self.update_graph)

    def change_period(self, period):
        #Change la période affichée (1J, 1S, 1M, ALL) et redessine.

        self.current_period = period
        self.redraw_for_period()

    def get_filtered_data(self):
        #Retourne les x/y filtrés selon la période actuelle.
        if not self.data_x:
            return [], []

        df = pd.DataFrame({"x": pd.to_datetime(self.data_x),"y": self.data_y})

        if self.current_period == "1J":
            cutoff = df["x"].max() - pd.Timedelta(days=1)
            df = df[df["x"] >= cutoff]
        elif self.current_period == "1S":
            cutoff = df["x"].max() - pd.Timedelta(days=7)
            df = df[df["x"] >= cutoff]
        elif self.current_period == "1M":
            cutoff = df["x"].max() - pd.Timedelta(days=30)
            df = df[df["x"] >= cutoff]

        # "ALL" = pas de filtre

        return list(df["x"]), list(df["y"])

    def redraw_for_period(self):
        #Redessine le graphique en fonction de la période choisie.
        x_vals, y_vals = self.get_filtered_data()
        self.dessiner_graph(x_vals, y_vals)

    def dessiner_graph(self, x_vals, y_vals):
        self.ax.clear()

        self.ax.set_facecolor("black")
        for spine in self.ax.spines.values():
            spine.set_color("white")
        self.ax.tick_params(axis='x', colors='white', rotation=45)
        self.ax.tick_params(axis='y', colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')

        self.ax.set_title("Rendement total du portefeuille")
        self.ax.set_ylabel("Rendement (%)")

        if len(x_vals) >= 2:
            # Segments rouge/vert selon la variation
            for i in range(1, len(x_vals)):
                prev = y_vals[i - 1]
                curr = y_vals[i]
                color = "green" if curr >= prev else "red"
                self.ax.plot(x_vals[i - 1:i + 1], [prev, curr],
                             color=color, linewidth=2)
        elif len(x_vals) == 1:
            # Un seul point -> simple scatter
            self.ax.scatter(x_vals, y_vals, color="white")

        self.canvas.draw()


    def retour_accueil(self):
        """Retour à l'écran d'accueil."""
        self.destroy()
        self.master.show_accueil()
