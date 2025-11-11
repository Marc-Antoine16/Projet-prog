import customtkinter as ctk
from titreDetenues import TitreDetenues
from placement import Placement
from creation import Creation
import json
import os
import yfinance as yf
from datetime import date

class Accueil(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.create_widgets()
       
    def create_widgets(self):

        self.master.grid_rowconfigure(0, weight= 1)
        self.master.grid_columnconfigure(0, weight= 1)

        # Le frame a plusieurs colonnes extensibles
        self.grid_rowconfigure((0, 1, 2,4,5,6,7,8,9,10), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5,6,7,8,9,10), weight=1)

        self.titre_label = ctk.CTkLabel(self, text="Accueil", font=("Arial", 32, "bold"))
        self.titre_label.grid(row=0, column=3, pady=(10,10))

        solde_total = self.calculer_solde_total()
    
        self.bouton_solde = ctk.CTkButton(self, text=f"solde total : {solde_total:.2f} $", font=("Arial", 20))
        self.bouton_solde.grid(row=1, column=3, pady=(10,10))

        self.bouton_titres = ctk.CTkButton(self, text= "Titres detenues ->", font=("Arial", 20), command= self.ouvrir_titreDetenues)
        self.bouton_titres.grid(row=3, column=3, pady=(10,10))

        self.compte_label = ctk.CTkLabel(self, text = "Compte(s)", font=("Arial", 24))
        self.compte_label.grid(row=5, column= 1, pady=(10,10))

        self.bouton_creation = ctk.CTkButton(self, text = "  Créer un compte", fg_color="transparent", hover_color="red", font=("Arial", 20), command =self.creer_compte)
        self.bouton_creation.grid(row = 6, column = 1, pady = (10,10))

        self.afficher_compte()

    def afficher_compte(self):
        if os.path.exists("comptes.json"):
            with open("comptes.json", "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

    
        if len(data) > 0:
                self.msgAide=ctk.CTkLabel(self, text=f"Compte créé ! Appuyer sur un de vos compte(s) pour commencer à négocier.", text_color="green", font=("Arial", 16))
                self.msgAide.grid(row=4,column = 3, pady=(10,10))
                comptes_afficher=data[-3:]
                for i, compte in enumerate(comptes_afficher):
                    nom = compte.get("nom", "Inconnu")
                    montant = compte.get("montant", 0)
                    self.bouton_compte = ctk.CTkButton(self,text=f"{nom} — {montant:.2f} $",font=("Arial", 20), command=lambda c=compte: self.ouvrir_infoCompte(c))
                    self.bouton_compte.grid(row=5 + i, column=3, pady=(10,10))
                return
        
        self.label_aucun = ctk.CTkLabel(self, text="Aucun compte n’a encore été créé.",font=("Arial", 20),text_color="gray")
        self.label_aucun.grid(row=5, column=3, pady=(10,10))

    def mettre_a_jour_solde(self):
        nouveau_solde = self.calculer_solde_total()
        self.bouton_solde.configure(text=f"Solde total : {nouveau_solde:.2f} $")

    def calculer_solde_total(self):
        total=0.0
        if os.path.exists("comptes.json"):
            with open("comptes.json","r") as f:
                try:
                    data= json.load(f)
                    total = sum(compte.get("montant", 0) for compte in data)
                except (json.JSONDecodeError, TypeError):
                    total =0.0
        return total
    
    def ouvrir_infoCompte(self, compte_data):
        #Ouvre la Watchlist du compte sélectionné avec ses données sauvegardées.
        self.clear_main_frame()
        from watchlist import Watchlist
        from compte import Compte
        import yfinance as yf
        from datetime import date

        #Recharger les tickers enregistrés dans la watchlist du compte
        watchlist_data = {}
        for ticker in compte_data.get("watchlist", []):
            try:
                df = yf.download(ticker, start="2024-01-01", end=date.today(), interval="1d")
                if not df.empty:
                    df["Close"] = df["Close"].astype(float)
                    watchlist_data[ticker] = df
            except Exception as e:
                print(f"Erreur lors du chargement du ticker {ticker} :", e)

        #Crée l'objet Compte correspondant au JSON
        compte = Compte(
            master=self.master,
            stocks=watchlist_data,              #les DataFrames rechargés ici
            temps=1,
            action=compte_data.get("actions", {}),
            argent=compte_data.get("montant", 0)
        )
        setattr(compte, "nom", compte_data.get("nom", "Inconnu"))

        #O«uvre la Watchlist propre à ce compte
        self.destroy()
        self.master.current_page = Watchlist(master=self.master, compte=compte, temps=1)
        self.master.current_page.grid(row=0, column=0, sticky="nsew")

        print(f"Compte '{compte.nom}' ouvert avec {len(watchlist_data)} titre(s) dans la Watchlist.")



 
        

    def ouvrir_titreDetenues(self):
        self.clear_main_frame()
        TitreDetenues(self.master)

    def ouvrir_placement(self):
        self.clear_main_frame()
        Placement(self.master)
    
    def creer_compte(self):

        if os.path.exists("comptes.json"):
            with open("comptes.json", "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

        if len(data)>2:
            self.msgAide.destroy()
            tropDeCompte=ctk.CTkLabel(self, text="Vous avez atteint le maximum de trois comptes !", text_color="red", font=("Arial", 16))
            tropDeCompte.grid(row=4,column = 3, pady=(10,10))
        else:
            self.clear_main_frame()
            Creation(self.master)

        

    def clear_main_frame(self):
            if hasattr(self, "boucle_id"):
                try:
                    self.after_cancel(self.boucle_id)
                except Exception:
                    pass

            for widget in self.winfo_children():
                widget.destroy()
    

        