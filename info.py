import customtkinter as ctk
import time

class Info(ctk.CTkFrame):
    def __init__(self, master = None, stocks = None, nom = None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.nom = nom
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        self.master.grid_rowconfigure(0, weight= 1)
        self.master.grid_columnconfigure(0, weight= 1)

        self.titre_label = ctk.CTkLabel(self, text="Statistiques", font=("Arial", 30, "bold"))
        self.titre_label.grid(row=1, column=0, padx = (10, 30), pady=(5,20))

        self.titre_nom = ctk.CTkLabel(self, text=self.nom, font=("Arial", 40, "bold"))
        self.titre_nom.grid(row=0, column=1, padx = (20, 20), pady=(5,20))

        self.titre_prix = ctk.CTkLabel(self, text= "Prix", font=("Arial", 30, "bold"))
        self.titre_prix.grid(row=1, column=2, padx = (30, 0), pady=(5,20))

        date = self.stocks[self.nom].index[0].date()
        self.date = ctk.CTkLabel(self, text=f"date : {date}", text_color= "light gray", font=("Arial", 20))
        self.date.grid(row=0, column=3, padx = (0, 50), pady=(5,10))

        self.categorie_open = ctk.CTkLabel(self, text= "Ouverture", text_color= "light gray", font = ("Arial", 24))
        self.categorie_open.grid(row = 2, column = 0, padx = (10, 40), pady = (10, 10))

        self.categorie_close = ctk.CTkLabel(self, text= "Fermeture", text_color= "light gray", font = ("Arial", 24))
        self.categorie_close.grid(row = 3, column = 0, padx = (10, 40), pady = (10, 10))

        self.categorie_high = ctk.CTkLabel(self, text= "High", text_color= "light gray", font = ("Arial", 24))
        self.categorie_high.grid(row = 4, column = 0, padx = (10, 40), pady = (10, 10))

        self.categorie_low = ctk.CTkLabel(self, text= "Low", text_color= "light gray", font = ("Arial", 24))
        self.categorie_low.grid(row = 5, column = 0, padx = (10, 40), pady = (10, 10))

        self.categorie_volume = ctk.CTkLabel(self, text= "Volume", text_color= "light gray", font = ("Arial", 24))
        self.categorie_volume.grid(row = 6, column = 0, padx = (10, 40), pady = (10, 10))

        self.categorie_pourcentage = ctk.CTkLabel(self, text= "Pourcentage", text_color= "light gray", font = ("Arial", 24))
        self.categorie_pourcentage.grid(row = 7, column = 0, padx = (10, 40), pady = (10, 10))

        self.categorie_variation = ctk.CTkLabel(self, text= "Variation", text_color= "light gray", font = ("Arial", 24))
        self.categorie_variation.grid(row = 8, column = 0, padx = (10, 40), pady = (10, 10))
        
        self.watchlist_button = ctk.CTkButton(self, text="retour", fg_color = "transparent", hover_color= "cyan", font=("Arial", 30, "bold"), command= self.retour)
        self.watchlist_button.grid(row=0, column=0, padx = (0, 0), pady = (5,20))

        self.boucle_stock(1)

    def boucle_stock(self, temps):
        if temps == len(self.stocks[next(iter(self.stocks))]['Close']):
            temps = 1
        
        else:
            for widget in self.winfo_children():
                    info = widget.grid_info()
                    col = info.get("column")
                    row = info.get("row")
                    if (col == 2 and row != (0 or 1)) or (col == 3 and row == 0):
                        widget.destroy()

            i = 2
            for stock in self.stocks:
                open = round(self.stocks[self.nom]['Open'].iloc[temps].iloc[0], 2)
                self.open = ctk.CTkLabel(self, text= open, text_color= "light gray", font = ("Arial", 24))
                self.open.grid(row = i, column = 2, padx = (40, 0), pady = (10, 10))

                close = round(self.stocks[self.nom]['Close'].iloc[temps].iloc[0], 2)
                self.close = ctk.CTkLabel(self, text= close, text_color= "light gray", font = ("Arial", 24))
                self.close.grid(row = 3, column = 2, padx = (40, 0), pady = (10, 10))
                
                high = round(self.stocks[self.nom]['High'].iloc[temps].iloc[0], 2)
                self.high = ctk.CTkLabel(self, text= high, text_color= "light gray", font = ("Arial", 24))
                self.high.grid(row = 4, column = 2, padx = (40, 0), pady = (10, 10))
                
                low = round(self.stocks[self.nom]['Low'].iloc[temps].iloc[0], 2)
                self.low = ctk.CTkLabel(self, text= low, text_color= "light gray", font = ("Arial", 24))
                self.low.grid(row = 5, column = 2, padx = (40, 0), pady = (10, 10))

                volume = round(self.stocks[self.nom]['Volume'].iloc[temps].iloc[0], 2)
                self.volume = ctk.CTkLabel(self, text= volume, text_color= "light gray", font = ("Arial", 24))
                self.volume.grid(row = 6, column = 2, padx = (30, 0), pady = (10, 10))
                
                pourcentage = round((close - open)/open * 100, 2)
                self.pourcentage = ctk.CTkLabel(self, text= f"{pourcentage} %", text_color= "light gray", font = ("Arial", 24))
                self.pourcentage.grid(row = 7, column = 2, padx = (40, 0), pady = (10, 10))

                variation = round((close - open), 2)
                self.variation = ctk.CTkLabel(self, text= variation, text_color= "light gray", font = ("Arial", 24))
                self.variation.grid(row = 8, column = 2, padx = (40, 0), pady = (10, 10))

                i += 1   

            self.date = ctk.CTkLabel(self, text=self.stocks[stock]. index[temps].date(), text_color= "light gray", font=("Arial", 24))
            self.date.grid(row=0, column=3, padx = (0, 10), pady=(10,10))
            self.boucle_id = self.after(5000, lambda: self.boucle_stock(temps + 1))

    def clear_main_frame(self):
        if hasattr(self, "boucle_id"):
            self.after_cancel(self.boucle_id)
            
        for widget in self.winfo_children():
            widget.destroy()
    
    def retour(self):
        from watchlist import Watchlist
        self.clear_main_frame()
        Watchlist(self.master, self.stocks)