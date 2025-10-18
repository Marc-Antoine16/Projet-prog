import customtkinter as ctk

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
        self.titre_label.grid(row=1, column=0, padx = (10, 50), pady=(5,10))
        self.titre_nom = ctk.CTkLabel(self, text=self.nom, font=("Arial", 30, "bold"))
        self.titre_nom.grid(row=1, column=1, padx = (50, 50), pady=(5,10))
        self.titre_prix = ctk.CTkLabel(self, text= "Prix", font=("Arial", 30, "bold"))
        self.titre_prix.grid(row=1, column=2, padx = (50, 0), pady=(5,10))
        date = self.stocks[self.nom].index[0].date()
        self.date = ctk.CTkLabel(self, text=f"date : {date}", text_color= "light gray", font=("Arial", 20))
        self.date.grid(row=0, column=3, padx = (0, 50), pady=(5,10))
        high = round(self.stocks[self.nom]['High'].iloc[0].iloc[0], 2)
        self.high = ctk.CTkLabel(self, text= f"High : {high}", text_color= "light gray", font = ("Arial", 20))
        self.high.grid(row = 2, column = 0, padx = (50, 50), pady = (10, 10))
        