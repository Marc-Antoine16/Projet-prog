import customtkinter as ctk
import json, os

class Compte(ctk.CTkFrame):
    def __init__(self, master = None, stocks = None, temps = None, action = None, argent = None, nom=None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.action = action if action is not None else {}
        self.temps = temps
        self.nom=nom
        self.argent = float(argent)

    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.master.grid_rowconfigure(0, weight= 1)
        self.master.grid_columnconfigure(0, weight= 1)

        self.titre_label = ctk.CTkLabel(self, text="Compte", font=("Arial", 30, "bold"))
        self.titre_label.grid(row=0, column=2, padx = (10, 30), pady=(5,20))
        
        self.date_label = ctk.CTkLabel(self, text="Compte", font=("Arial", 30, "bold"))

        self.argent_label = ctk.CTkLabel(self, text=f"{self.argent:.2f} $", font=("Arial", 20, "bold"))
        self.argent_label.grid(row=0, column=5, padx=10, pady=5)

        self.watchlist_button = ctk.CTkButton(self, text="retour", fg_color = "transparent", hover_color= "cyan", font=("Arial", 30, "bold"), command= self.retour)
        self.watchlist_button.grid(row=0, column=0, padx = (0, 0), pady = (5,20))

        tittles = ["Action", "Quantité", "Prix d'achat", "Prix actuel", "Évolution (%)"]
        for col, text in enumerate(tittles):
            titre = ctk.CTkLabel(self, text=text, font=("Arial", 20, "bold"))
            titre.grid(row=1, column=col, padx=10, pady=(10, 20))

        i = 2
        for nom, info in self.action.items():
            prix_achat = info["prix_achat"]

            prix_actuel = round(info["data"]["Close"].iloc[self.temps].iloc[0], 2) if self.temps < len(info["data"]["Close"]) else round(info["data"]["Close"].iloc[-1].iloc[0], 2)

            pourcentage = round(float((prix_actuel - prix_achat) / prix_achat) * 100, 2)

            couleur = "green" if pourcentage >= 0 else "red"

            quantite = info["quantite"]

            ctk.CTkLabel(self, text=nom, font=("Arial", 20, "bold")).grid(row=i, column=0, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{quantite}", font=("Arial", 15)).grid(row=i, column=1, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{prix_achat:.2f} $", font=("Arial", 15)).grid(row=i, column=2, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{prix_actuel:.2f} $", font=("Arial", 15)).grid(row=i, column=3, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{pourcentage:+.2f} %", font=("Arial", 15), text_color=couleur).grid(row=i, column=4, padx=10, pady=5)

            bouton_vendre = ctk.CTkButton(self, text="Vendre", fg_color="transparent", hover_color="red", font=("Arial", 15), command=lambda a=nom: self.vendre_action(a))
            bouton_vendre.grid(row=i, column=5, padx=0, pady=5)

            i += 1
            
        self.update_affichage()

    def update_affichage(self):
        if self.temps == len(self.stocks[next(iter(self.stocks))]['Close']):
            self.temps = 1

        else:
            for widget in self.winfo_children():
                info = widget.grid_info()
                col = info.get("column")
                row = info.get("row")
                if (col in (3, 4) and row >= 2) or (row == 0 and col in (4, 5)):
                    widget.destroy()

            i = 2
            for nom, info in self.action.items():
                prix_achat = float(info["prix_achat"])

                t = int(self.temps)
                if t < len(info["data"]["Close"]):
                    prix_actuel = float(round(info["data"]["Close"].iloc[t].iloc[0], 2))
                else:
                    prix_actuel = float(round(info["data"]["Close"].iloc[-1].iloc[0], 2))

                pourcentage = round(((prix_actuel - prix_achat) / prix_achat) * 100, 2)
                couleur = "green" if pourcentage >= 0 else "red"
                quantite = info["quantite"]

                ctk.CTkLabel(self, text=nom, font=("Arial", 20, "bold")).grid(row=i, column=0, padx=10, pady=5)
                ctk.CTkLabel(self, text=f"{quantite}", font=("Arial", 15)).grid(row=i, column=1, padx=10, pady=5)
                ctk.CTkLabel(self, text=f"{prix_achat:.2f} $", font=("Arial", 15)).grid(row=i, column=2, padx=10, pady=5)
                ctk.CTkLabel(self, text=f"{prix_actuel:.2f} $", font=("Arial", 15)).grid(row=i, column=3, padx=10, pady=5)
                ctk.CTkLabel(self, text=f"{pourcentage:+.2f} %", font=("Arial", 15), text_color=couleur).grid(row=i, column=4, padx=10, pady=5)

                i += 1
            
            if len(self.stocks) > 0:
                premier_stock = next(iter(self.stocks))
                self.date = ctk.CTkLabel(self, text=self.stocks[premier_stock].index[self.temps].date(), text_color="light gray", font=("Arial", 24))
                self.date.grid(row=0, column=4, padx=(0, 10), pady=(10,10))
            self.argent_label = ctk.CTkLabel(self, text=f"{self.argent:.2f} $", font=("Arial", 20, "bold"))
            self.argent_label.grid(row=0, column=5, padx=10, pady=5)
            self.temps += 1
            self.boucle_id = self.after(5000, lambda: self.update_affichage())

    def clear_main_frame(self):
        if hasattr(self, "boucle_id"):
            self.after_cancel(self.boucle_id)
            
        for widget in self.winfo_children():
            widget.destroy()

    def vendre_action(self, action):
        """Vend une action, met à jour le solde, le JSON et l'affichage."""
        if action not in self.action:
            print(f"[ERREUR] L'action {action} n'existe pas dans le compte.")
            return

        info = self.action[action]

        #Récupère le prix actuel
        if "data" in info and not info["data"].empty:
            if self.temps < len(info["data"]["Close"]):
                prix_actuel = float(info["data"]["Close"].iloc[self.temps].item())
            else:
                prix_actuel = float(info["data"]["Close"].iloc[-1].item())
        else:
            import yfinance as yf
            from datetime import date
            df = yf.download(action, start="2024-01-01", end=date.today(), interval="1d")
            if not df.empty:
                prix_actuel = float(df["Close"].iloc[-1])
            else:
                print(f"ERREUR Impossible d'obtenir le prix de {action}.")
                return

        #Mise à jour des montants
        self.argent += prix_actuel
        info["quantite"] -= 1

        #Suppression si plus d'actions
        if info["quantite"] <= 0:
            del self.action[action]

        # Sauvegarde  dans comptes.json
        self.sauvegarder()
        print(f"[OK] Vente sauvegardée : {action} vendu, solde = {self.argent:.2f}$")

        #Rafraîchir l'affichage
        for widget in self.winfo_children():
            grid_info = widget.grid_info()
            if grid_info.get("row", 0) >= 2:
                widget.destroy()

        i = 2
        for nom, infos in self.action.items():
            prix_achat = float(infos["prix_achat"])
            if "data" in infos and not infos["data"].empty:
                prix_actuel = float(round(infos["data"]["Close"].iloc[-1].item(), 2))
            else:
                prix_actuel = prix_achat
            pourcentage = round(((prix_actuel - prix_achat) / prix_achat) * 100, 2)
            couleur = "green" if pourcentage >= 0 else "red"

            ctk.CTkLabel(self, text=nom, font=("Arial", 20, "bold")).grid(row=i, column=0, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{infos['quantite']}", font=("Arial", 15)).grid(row=i, column=1, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{prix_achat:.2f} $", font=("Arial", 15)).grid(row=i, column=2, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{prix_actuel:.2f} $", font=("Arial", 15)).grid(row=i, column=3, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{pourcentage:+.2f} %", font=("Arial", 15), text_color=couleur).grid(row=i, column=4, padx=10, pady=5)

            ctk.CTkButton(self, text="Vendre", fg_color="transparent", hover_color="red",
                        font=("Arial", 15), command=lambda a=nom: self.vendre_action(a)).grid(row=i, column=5, padx=0, pady=5)
            i += 1

        self.argent_label.configure(text=f"{self.argent:.2f} $")

        # Confirmation visuell
        confirmation = ctk.CTkLabel(self, text=f"{action} vendue (+{prix_actuel:.2f}$)", text_color="green", font=("Arial", 16))
        confirmation.grid(row=i, column=3, pady=10)
        self.after(3000, confirmation.destroy)


   



    def retour(self):
        from watchlist import Watchlist
        nouveau_compte = Compte(self.master, self.stocks, self.temps, self.action, self.argent)
        self.clear_main_frame()
        Watchlist(self.master, self.stocks, self.temps, nouveau_compte)

    def sauvegarder(self):
        """Sauvegarde le compte sans inclure les DataFrames (non sérialisables)."""
        if not hasattr(self, "nom"):
            print("ERREUR Impossible de sauvegarder : le compte n'a pas de nom.")
            return

        #Crée une version simplifiée des actions (sans les DataFrames)
        actions_simplifiee = {}
        for symbole, infos in self.action.items():
            actions_simplifiee[symbole] = {
                "prix_achat": float(infos["prix_achat"]),
                "quantite": int(infos["quantite"])
            }

        #Simplifie la watchlist
        watchlist_simplifiee = list(self.stocks.keys()) if self.stocks else []

        #Lire le fichier existant
        comptes = []
        if os.path.exists("comptes.json"):
            with open("comptes.json", "r") as f:
                try:
                    comptes = json.load(f)
                except json.JSONDecodeError:
                    comptes = []

        #Mettre à jour ou ajouter le compte
        compte_trouve = False
        for i, c in enumerate(comptes):
            if c["nom"] == self.nom:
                comptes[i]["montant"] = float(self.argent)
                comptes[i]["actions"] = actions_simplifiee   #sauvegarde bien la version à jour
                comptes[i]["watchlist"] = watchlist_simplifiee
                compte_trouve = True
                break

        if not compte_trouve:
            comptes.append({
                "nom": self.nom,
                "montant": float(self.argent),
                "actions": actions_simplifiee,
                "watchlist": watchlist_simplifiee
            })

        #Écrire le fichier
        with open("comptes.json", "w") as f:
            json.dump(comptes, f, indent=4)

        print(f"[OK] Compte '{self.nom}' sauvegardé : {len(actions_simplifiee)} action(s).")
