import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors



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

        fig, ax = plt.subplots(figsize=(9,6))
        line, = ax.plot(x, y, linestyle='-', color='dodgerblue')
        ax.set_xlabel("Date")
        ax.set_ylabel("Prix")
    
        ax.set_facecolor("black")

        ax.grid(False)
        ax.tick_params(colors='white')                 # Couleur des ticks (valeurs sur les axes)
        ax.xaxis.label.set_color('white')              # Label de l'axe X (Date)
        ax.yaxis.label.set_color('white')              # Label de l'axe Y (Prix)
        ax.title.set_color('white')

        for spine in ax.spines.values():
            spine.set_color('white')

        fig.patch.set_facecolor('black') #figure autour du graphique
        
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