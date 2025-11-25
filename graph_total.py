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
    UPDATE_INTERVAL = 5000  # mise à jour toutes les 5 secondes

    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.data_x = []  # timestamps
        self.data_y = []  # rendements

        # Cache pour les DataFrames yfinance
        self.df_cache = {}

        self.load_history()
        self.create_widgets()
        self.update_graph()  # lance la mise à jour en boucle

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
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2,sticky="nsew", pady=20)

        # Bouton retour
        btn_retour = ctk.CTkButton(self,text="← Retour",fg_color="transparent",hover_color="green",font=("Arial", 20),command=self.retour_accueil)
        btn_retour.grid(row=0, column=0, padx=10, pady=10, sticky="w")


    def load_history(self):
        """Charge l'historique du rendement total depuis le JSON, si dispo."""
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
        """Ajoute un point de rendement dans le fichier d'historique."""
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


    def charger_comptes(self):
        if not os.path.exists("comptes.json"):
            return []

        try:
            with open("comptes.json", "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []

    def get_df_symbole(self, symbole):
        """Retourne le DataFrame yfinance pour un symbole (avec cache)."""
        if symbole in self.df_cache:
            return self.df_cache[symbole]

        try:
            df = yf.download(symbole, start="2024-01-01", interval="1d", progress=False)
            if df.empty or "Close" not in df:
                print(f"[ATTENTION] Aucune donnée valide pour {symbole}")
                self.df_cache[symbole] = None
                return None

            df["Close"] = df["Close"].astype(float)
            self.df_cache[symbole] = df
            return df

        except Exception as e:
            print(f"[ERREUR] Téléchargement {symbole} : {e}")
            self.df_cache[symbole] = None
            return None

    def calcul_rendement_total(self):

        comptes = self.charger_comptes()
        if not comptes:
            return 0.0

        t = int(getattr(self.master, "jour_global", 0))

        total_investi = 0.0
        total_valeur = 0.0

        for compte in comptes:
            actions = compte.get("actions", {})

            for symbole, info in actions.items():
                quantite = info.get("quantite", 0)
                prix_achat = float(info.get("prix_achat", 0))

                if quantite <= 0 or prix_achat <= 0:
                    continue

                df = self.get_df_symbole(symbole)
                if df is None:
                    # si aucune donnée, ignore ce titre pour le rendement
                    continue

                serie = df["Close"]
                if len(serie) == 0:
                    continue

                idx = t
                if idx >= len(serie):
                    idx = len(serie) - 1

                prix_actuel = float(serie.iloc[idx])

                total_investi += prix_achat * quantite
                total_valeur += prix_actuel * quantite

        if total_investi == 0:
            return 0.0

        rendement = ((total_valeur - total_investi) / total_investi) * 100
        return float(rendement)


    def update_graph(self):
        """Ajoute un point, sauvegarde, et redessine selon la période."""

        if not self.winfo_exists():
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rendement = self.calcul_rendement_total()

        self.data_x.append(timestamp)
        self.data_y.append(rendement)
        self.save_point(timestamp, rendement)

        MAX_POINTS = 10
        if len(self.data_x) > MAX_POINTS:
            x_vals = self.data_x[-MAX_POINTS:]
            y_vals = self.data_y[-MAX_POINTS:]
        else:
            x_vals = self.data_x
            y_vals = self.data_y

        self.dessiner_graph(x_vals, y_vals)

        if hasattr(self.master, "jour_global"):
            max_len = 999999
            for compte in self.charger_comptes():
                for sym, info in compte.get("actions", {}).items():
                    df = self.get_df_symbole(sym)
                    if df is not None:
                        max_len = min(max_len, len(df["Close"]))
            
            if self.master.jour_global < max_len -1:
                self.master.jour_global+=1


        # Replanifie l'update
        self.after(self.UPDATE_INTERVAL, self.update_graph)


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
            for i in range(1, len(x_vals)):
                prev = y_vals[i - 1]
                curr = y_vals[i]
                color = "green" if curr >= prev else "red"
                self.ax.plot(x_vals[i - 1:i + 1], [prev, curr], color=color, linewidth=2)
                
        elif len(x_vals) == 1:
            self.ax.scatter(x_vals, y_vals, color="white")

        self.canvas.draw()

    def retour_accueil(self):
        """Retour à l'écran d'accueil."""
        self.destroy()
        if hasattr(self.master, "show_accueil"):
            self.master.show_accueil()
