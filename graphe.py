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

        self.master.grid_rowconfigure(0, weight= 1)
        self.master.grid_columnconfigure(0, weight= 1)

        x = self.stocks[self.nom].index
        y = self.stocks[self.nom]["Close"]

        fig, ax = plt.subplots(figsize=(9,6))
        line, = ax.plot(x, y, linestyle='-', color='dodgerblue')
        ax.set_xlabel("Date")
        ax.set_ylabel("Prix")
    
        ax.set_facecolor("black")
             
        fig.patch.set_facecolor("black")  # Fond de la figure
        ax.set_facecolor("black")         # Fond de la zone du graphe

        # Couleur des axes et labels
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')

        # Couleur du texte et des ticks (graduations)
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Titre et étiquettes optionnelles
        ax.title.set_color('white')

        ax.grid(False)

        lines = []
        for i in range(1, len(x)):
            prev_val = float(y.iloc[i - 1])
            curr_val = float(y.iloc[i])
            color = "green" if curr_val > prev_val else "red"
            l, = ax.plot(x[i - 1:i + 1], y.iloc[i - 1:i + 1], color=color, linewidth=2)
            lines.append(l)

        price_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, ha='left', va='top', fontsize=30, bbox=dict(boxstyle="round", fc="none", alpha=0))


        cursor = mplcursors.cursor(line, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            sel.annotation.set_visible(False)
            price_text.set_text(f"Prix : {sel.target[1]:.2f}")
            price_text.set_color("lightgray")
            self.canvas.draw_idle()

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master = self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 1, column= 0, columnspan=3, pady=(10, 10))

        self.frame_periodes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_periodes.grid(row=2, column=0, columnspan=3, pady=(20, 10), sticky="ew")

        self.frame_periodes.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        periodes = ["1J", "1M", "3M", "1A", "5A"]
        for i, p in enumerate(periodes):
            bouton = ctk.CTkButton(self.frame_periodes,text=p,fg_color="transparent",hover_color="gray30",font=("Arial", 18, "bold"),command=lambda per=p: self.afficher_periode(per) )
            bouton.grid(row=0, column=i, padx=10, pady=5, sticky="ew")

        self.watchlist_button = ctk.CTkButton(self, text="retour", fg_color = "transparent", hover_color= "light green", font=("Arial", 15, "bold"), command= self.retour)
        self.watchlist_button.grid(row=0, column=0, pady=(0,0))

    def afficher_periode(self, periode):
        data = self.stocks[self.nom]
        if len(data) < 2:
            return

        if periode == "1J":
            df_filtre = data.tail(2)
        elif periode == "1M":
            df_filtre = data[data.index > (data.index[-1] - pd.DateOffset(months=1))]
        elif periode == "3M":
            df_filtre = data[data.index > (data.index[-1] - pd.DateOffset(months=3))]
        elif periode == "1A":
            df_filtre = data[data.index > (data.index[-1] - pd.DateOffset(years=1))]
        elif periode == "5A":
            df_filtre = data[data.index > (data.index[-1] - pd.DateOffset(years=5))]
        else:
            df_filtre = data

        self.redessiner_graphique(df_filtre)

    def redessiner_graphique(self, df):
        # Supprime ancien graphique
        for widget in self.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        x = df.index
        y = df["Close"]

        fig, ax = plt.subplots(figsize=(9, 6))
        fig.patch.set_facecolor("black")
        ax.set_facecolor("black")

        for spine in ax.spines.values():
            spine.set_color("white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.title.set_color("white")
        ax.grid(False)

        if len(x) > 1:
            for i in range(1, len(x)):
                prev_val = float(y.iloc[i - 1])
                curr_val = float(y.iloc[i])
                color = "green" if curr_val > prev_val else "red"
                ax.plot(x[i - 1:i + 1], y.iloc[i - 1:i + 1], color=color, linewidth=2)
        else:
                ax.plot(x, y, color="dodgerblue", linewidth=2)

        dernier_prix = y.iloc[-1]
        ax.text(0.05, 0.95, f"Prix : {dernier_prix:.2f}",transform=ax.transAxes,ha='left', va='top', fontsize=30, color='lightgray')
            
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, pady=(10, 10))

   

    def clear_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def retour(self):
        from watchlist import Watchlist
        self.clear_main_frame()
        Watchlist(self.master, self.stocks, self.temps, self.compte)