import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors
import pandas as pd


class Graph(ctk.CTkFrame):
    def __init__(self, master=None, stocks = None, nom = None, temps = None, compte = None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.nom = nom
        self.temps = temps
        self.compte = compte
        self.create_widgets()


    def create_widgets(self):
        self.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        #Graphique initiale
        self.fig, self.ax = plt.subplots(figsize=(9, 6))
        self.fig.patch.set_facecolor("black")
        self.ax.set_facecolor("black")

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')

        #canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, pady=(10, 10))

        #Boutons périodes
        self.frame_periodes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_periodes.grid(row=2, column=0, columnspan=3, pady=(20, 10), sticky="ew")
        self.frame_periodes.grid_columnconfigure((0, 1, 2), weight=1)

        periodes = ["1M", "3M", "1A"]
        for i, p in enumerate(periodes):
            bouton = ctk.CTkButton(self.frame_periodes,text=p,fg_color="transparent",hover_color="gray30",font=("Arial", 18, "bold"),command=lambda per=p: self.afficher_periode(per))
            bouton.grid(row=0, column=i, padx=10, pady=5, sticky="ew")

        #Bouton retour
        self.watchlist_button = ctk.CTkButton(self, text="Retour",fg_color="transparent",hover_color="light green",font=("Arial", 15, "bold"),command=self.retour)
        self.watchlist_button.grid(row=0, column=0, pady=(0, 0))

        # Affiche le graphique par défaut
        self.afficher_periode("1A")


    def afficher_periode(self, periode):
        data = self.stocks[self.nom]
        if len(data) < 2:
            return

        if periode == "1M":
            df_filtre = data[data.index > (data.index[-1] - pd.DateOffset(months=1))] #fonction de pandas qui créer un décalage temporel (offset) de 1 mois
        elif periode == "3M":
            df_filtre = data[data.index > (data.index[-1] - pd.DateOffset(months=3))]
        elif periode == "1A":
            df_filtre = data[data.index > (data.index[-1] - pd.DateOffset(years=1))]
        else:
            df_filtre = data

        self.redessiner_graphique(df_filtre, periode)


    def redessiner_graphique(self, df, periode):
        self.ax.clear()

        self.ax.set_facecolor("black")
        for spine in self.ax.spines.values():
            spine.set_color("white")
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        self.ax.grid(False)

        x = df.index
        y = df["Close"]

        # Petite fonction pour convertir correctement les valeurs sinon erreur
        def to_float(v):
            if hasattr(v, "iloc"): #sert à vérifier si un objet possède un attribut
                return float(v.iloc[0])
            return float(v)

        # Tracé coloré vert/rouge
        line_segments = []
        for i in range(1, len(x)): #par segment
            prev_val = to_float(y.iloc[i - 1])
            curr_val = to_float(y.iloc[i])
            if curr_val > prev_val:
                color = "green"
            else:
                color="red"

            (l,) = self.ax.plot(x[i - 1:i + 1], [prev_val, curr_val], color=color, linewidth=2) #trace petit segment de courbe entre x[i-1] et x[i]
            line_segments.append(l)

    
        #Curseur interactif
        cursor = mplcursors.cursor(line_segments, hover=True)
        price_text = self.ax.text(0.05, 0.90, "",transform=self.ax.transAxes,ha='left', va='top',fontsize=20, color='lightgray')

        @cursor.connect("add")
        def on_add(sel):
            sel.annotation.set_visible(False)
            price_text.set_text(f"Prix : {sel.target[1]:.2f}")
            self.canvas.draw_idle()

        self.canvas.draw_idle()


        

    def clear_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
        
    def retour(self):
        from watchlist import Watchlist
        self.clear_main_frame()
        Watchlist(self.master, self.stocks, self.temps, self.compte)