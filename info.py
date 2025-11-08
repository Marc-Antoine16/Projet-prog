import customtkinter as ctk
import pandas as pd
import time
import yfinance as yf
import webbrowser
from gnews import GNews

class Info(ctk.CTkFrame):
    def __init__(self, master = None, stocks = None, nom = None, temps = None, compte = None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.nom = nom
        self.stock = yf.Ticker(self.nom)
        self.temps = temps
        self.compte = compte
        self.nbColonnes = 3
        self.nbLignes = 8
        # self.nouvelles = pd.DataFrame(self.stock.news[:5])[["title", "publisher", "link"]]
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        for i in range(self.nbColonnes):
            self.master.grid_columnconfigure(i, weight= 1)
        
        for i in range(self.nbLignes):
            self.master.grid_rowconfigure(i, weight= 1)

        self.watchlist_button = ctk.CTkButton(self, text="retour", fg_color = "transparent", hover_color= "light gray", border_width=2, border_color="white",  font=("Arial", 30, "bold"), command= self.retour)
        self.watchlist_button.grid(row=0, column=0, padx = (0, 0), pady = (5,20), sticky="w")

        self.titre_nom = ctk.CTkLabel(self, text=f"{self.nom} - {self.stock.info["longName"]}", justify="center", anchor="center", font=("Arial", 30, "bold"))
        self.titre_nom.grid(row=0, column=1, padx = (20, 20), pady=(5,20))

        self.ligne1 = ctk.CTkFrame(self, height=2, width=300, fg_color="gray")
        self.ligne1.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")

        self.titre_label = ctk.CTkLabel(self, text="Statistiques", font=("Arial", 28, "bold"))
        self.titre_label.grid(row=2, column=0, padx = (10, 30), pady=20)

        self.titre_prix = ctk.CTkLabel(self, text= "Prix", font=("Arial", 28, "bold"))
        self.titre_prix.grid(row=2, column=1, padx = (30, 0), pady=20)

        self.titre_nouvelles = ctk.CTkLabel(self, text= "Nouvelles récentes", font=("Arial", 28, "bold"))
        self.titre_nouvelles.grid(row=2, column=2, padx = (30, 100), pady=20, sticky="e")

        self.ligne2 = ctk.CTkFrame(self, height=2, width=300, fg_color="gray")
        self.ligne2.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

        google_news = GNews(language='fr', country='CA', period='7d')
        nouvelles = google_news.get_news(self.nom)

        if not nouvelles:
            aucun_label = ctk.CTkLabel(self, text="Aucune nouvelle récente disponible.", font=("Arial", 18))
            aucun_label.grid(row=4, column=2, padx=(30, 100), pady=20, sticky="w")
        else:
            i = 4
            for nouvelle in nouvelles[:5]:
                titre = nouvelle['title']
                lien = nouvelle['url']
                source = nouvelle.get('publisher', {}).get('title', 'Source inconnue')

                self.nouvelle_label = ctk.CTkLabel(self, text=f"• {titre}\n({source})", text_color="#1E90FF", cursor="hand2", font=("Arial", 20), justify="left", wraplength=600)
                self.nouvelle_label.grid(row=i, column=2, padx=30, pady=(5, 10), sticky="w")
                self.nouvelle_label.bind("<Button-1>", lambda e, url=lien: webbrowser.open(url))

                i += 1

        self.boucle_stock()

    def boucle_stock(self):
        if self.temps == len(self.stocks[next(iter(self.stocks))]['Close']):
            self.temps = 1
        
        else:
            for widget in self.winfo_children():
                    info = widget.grid_info()
                    col = info.get("column")
                    row = info.get("row")
                    if (col == 2 and row == 0) or (col == (0 or 1) and row >= 4):
                        widget.destroy()

            for stock in self.stocks:

                self.open = round(self.stocks[self.nom]['Open'].iloc[self.temps].iloc[0], 2)
                self.open_Label = ctk.CTkLabel(self, text= f"{"Ouverture :":<12}{self.open:4}", text_color= "light gray", font = ("Arial", 24))
                self.open_Label.grid(row = 4, column = 0, padx = (10, 30), pady = (10, 10), sticky="w")

                self.close = round(self.stocks[self.nom]['Close'].iloc[self.temps].iloc[0], 2)
                self.close_Label = ctk.CTkLabel(self, text= f"{"Fermeture :":<12}{self.close:<4}", text_color= "light gray", font = ("Arial", 24))
                self.close_Label.grid(row = 5, column = 0, padx = (10, 30), pady = (10, 10), sticky="w")
                
                self.high = round(self.stocks[self.nom]['High'].iloc[self.temps].iloc[0], 2)
                self.high_Label = ctk.CTkLabel(self, text= f"{"Haut :":<12}{self.high:<4}", text_color= "light gray", font = ("Arial", 24))
                self.high_Label.grid(row = 6, column = 0, padx = (10, 30), pady = (10, 10), sticky="w")
                
                self.low = round(self.stocks[self.nom]['Low'].iloc[self.temps].iloc[0], 2)
                self.low_Label = ctk.CTkLabel(self, text= f"{"Bas :":<12}{self.low:<4}", text_color= "light gray", font = ("Arial", 24))
                self.low_Label.grid(row = 7, column = 0, padx = (10, 30), pady = (10, 10), sticky="w")

                self.volume = round(self.stocks[self.nom]['Volume'].iloc[self.temps].iloc[0], 2)
                self.volume_Label = ctk.CTkLabel(self, text= f"{"Volume :":<12}{self.volume:<4}", text_color= "light gray", font = ("Arial", 24))
                self.volume_Label.grid(row = 4, column = 1, padx = (30, 30), pady = (10, 10), sticky="w")
                
                self.pourcentage = round((self.close - self.open)/self.open * 100, 2)
                self.pourcentage_Label = ctk.CTkLabel(self, text= f"{"Pourcentage :":<15}{self.pourcentage:<4}%", text_color= "light gray", font = ("Arial", 24))
                self.pourcentage_Label.grid(row = 5, column = 1, padx = (30, 30), pady = (10, 10), sticky="w")

                self.variation = round((self.close - self.open), 2)
                self.variation_Label = ctk.CTkLabel(self, text= f"{"Variation :":<15}{self.variation:<4}", text_color= "light gray", font = ("Arial", 24))
                self.variation_Label.grid(row = 6, column = 1, padx = (30, 30), pady = (10, 10), sticky="w")
  

            self.date = ctk.CTkLabel(self, text=self.stocks[stock]. index[self.temps].date(), text_color= "light gray", font=("Arial", 24))
            self.date.grid(row=0, column=2, padx = (100, 100), pady=(5,10), sticky="e")
            self.temps += 1
            self.boucle_id = self.after(5000, lambda: self.boucle_stock())

    def clear_main_frame(self):
        if hasattr(self, "boucle_id"):
            self.after_cancel(self.boucle_id)
            
        for widget in self.winfo_children():
            widget.destroy()
    
    def retour(self):
        from watchlist import Watchlist
        self.clear_main_frame()
        Watchlist(self.master, self.stocks, self.temps, self.compte)