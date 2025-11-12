import customtkinter as ctk
import os
import yfinance as yf
import json

class TitreDetenues(ctk.CTkFrame):
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

        titre_label = ctk.CTkLabel(self,text="Titres détenus",font=("Arial", 28, "bold") )
        titre_label.grid(row=0,column=2, pady=(10,10))

        btn_retour = ctk.CTkButton(self, text="← Retour", fg_color="transparent",hover_color="green", font=("Arial", 20),command=self.retour_accueil)
        btn_retour.grid(row=0, column=0, pady=(10, 10))

        self.afficher_titres()

    def afficher_titres(self):
        if not os.path.exists("comptes.json"):
            ctk.CTkLabel(self, text= "Aucun compte trouvé.", text_color="gray" ).grid(row=2, column=2)
            return

        with open("comptes.json", "r") as f:
            try:
                comptes=json.load(f)
            except json.JSONDecodeError:
                compte=[]
        
        if not comptes:
            ctk.CTkLabel(self, text="Aucun compte valide.", text_color="gray").grid(row=2, column=2)
            return
        
        titres={}
        for compte in comptes:
            actions= compte.get("actions", {})
            for symbole, data in actions.items():
                prix_achat=data.get("prix_achat", 0)
                quantite=data.get("quantite", 0)
                if quantite <=0 or prix_achat <=0:
                    continue
                # Si l’action existe déjà (détenue dans plusieurs comptes)
                if symbole in titres:
                    titres[symbole]["quantite"]+=quantite
                    titres[symbole]["prix_achat_total"]+= prix_achat * quantite
                else:
                    titres[symbole] = {"quantite":quantite, "prix_achat_total":prix_achat*quantite}

        if not titres:
            ctk.CTkLabel(self, text="Aucune action détenue.", text_color="gray").grid(row=3, column=2)
            return
        
        # En-têtes
        headers = ["Symbole", "Prix actuel ($)", "Rendement (%)"]
        for j, h in enumerate(headers):
            ctk.CTkLabel(self, text=h, font=("Arial", 20, "bold")).grid(row=2, column=j+1, padx=10, pady=10)
        
        row=3
        for symbole, infos in titres.items():
            try:
                ticker = yf.Ticker(symbole)
                prix_actuel = round(float(ticker.history(period="1d")["Close"].iloc[-1]), 2)
                prix_moyen_achat = infos["prix_achat_total"] / infos["quantite"]
                rendement = ((prix_actuel - prix_moyen_achat) / prix_moyen_achat) * 100
                couleur = "green" if rendement >= 0 else "red"
            except Exception as e:
                print(f"Erreur chargement {symbole}: {e}")
                prix_actuel = 0.0
                rendement = 0.0
                couleur = "gray"

            ctk.CTkLabel(self, text=symbole, font=("Arial", 18)).grid(row=row, column=1, pady=5)
            ctk.CTkLabel(self, text=f"{prix_actuel:.2f}", font=("Arial", 18)).grid(row=row, column=2, pady=5)
            ctk.CTkLabel(self, text=f"{rendement:.2f}%", text_color=couleur, font=("Arial", 18)).grid(row=row, column=3, pady=5)
            row += 1

    def retour_accueil(self):
        from accueil import Accueil
        self.destroy()
        self.master.current_page = Accueil(master=self.master)
        self.master.current_page.grid(row=0, column=0, sticky="nsew")

