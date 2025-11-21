import customtkinter as ctk
import yfinance as yf

class Compte(ctk.CTkFrame):
    def __init__(self, master=None, stocks=None, temps=None, action=None, argent=None, user=None, compte=None, watchlist=None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks or {}
        self.actions = action if action is not None else {}  
        self.temps = temps if temps is not None else 0
        self.argent = float(argent) if argent is not None else 0.0
        self.user = user
        self.compte = compte
        self.watchlist = watchlist 

        # S'assurer que self.actions contient au moins les infos de user.stocks_owned
        if self.user and self.user.stocks_owned:
            for nom, info_json in self.user.stocks_owned.items():
                if nom not in self.actions:
                    self.actions[nom] = {
                        "prix_achat": info_json["prix_achat"],
                        "quantite": info_json["quantite"],
                      
                    }

        self.create_widgets()

    # s'assurer que data est présent en MÉMOIRE SEULEMENT ----------
    def ensure_data_for_action(self, nom, info):
        if "data" in info and info["data"] is not None:
            return

        # Si le DataFrame est déjà dans self.stocks (watchlist), on s'en sert
        if self.stocks and nom in self.stocks:
            info["data"] = self.stocks[nom]
            return

        # 2) Sinon, on télécharge via yfinance
        try:
            df = yf.download(nom, start="2024-01-01", end="2025-10-11", interval="1d")
            df["Close"] = df["Close"].astype(float)
            info["data"] = df
        except Exception as e:
            print(f"Erreur téléchargement pour {nom} dans Compte :", e)
            info["data"] = None

    def create_widgets(self):
        # Layout de base
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        for i in range(6):
            self.grid_columnconfigure(i, weight=1)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.titre_label = ctk.CTkLabel(self, text="Compte", font=("Arial", 30, "bold"))
        self.titre_label.grid(row=0, column=2, padx=(10, 30), pady=(5, 20))

   
        self.argent_label = ctk.CTkLabel(self, text=f"{self.argent:.2f} $", font=("Arial", 20, "bold"))
        self.argent_label.grid(row=0, column=5, padx=10, pady=5)

        self.watchlist_button = ctk.CTkButton(
            self, text="retour", fg_color="transparent", hover_color="cyan",
            font=("Arial", 30, "bold"), command=self.retour
        )
        self.watchlist_button.grid(row=0, column=0, padx=(0, 0), pady=(5, 20))

        tittles = ["Action", "Quantité", "Prix d'achat", "Prix actuel", "Évolution (%)"]
        for col, text in enumerate(tittles):
            titre = ctk.CTkLabel(self, text=text, font=("Arial", 20, "bold"))
            titre.grid(row=1, column=col, padx=10, pady=(10, 20))

        i = 2
        actions_a_supprimer = []

        for nom, info in self.actions.items():
            quantite = info.get("quantite", 0)
            prix_achat = float(info.get("prix_achat", 0))

            if quantite <= 0:
                actions_a_supprimer.append(nom)
                continue

            # S'assurer qu'on a un DataFrame en mémoire
            self.ensure_data_for_action(nom, info)
            if info["data"] is None:
                continue

            df_close = info["data"]["Close"]

            if self.temps < len(df_close):
                prix_actuel = round(float(df_close.iloc[self.temps]), 2)
            else:
                prix_actuel = round(float(df_close.iloc[-1]), 2)

            pourcentage = round(((prix_actuel - prix_achat) / prix_achat) * 100, 2) if prix_achat != 0 else 0.0
            couleur = "green" if pourcentage >= 0 else "red"

            ctk.CTkLabel(self, text=nom, font=("Arial", 20, "bold")).grid(row=i, column=0, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{quantite}", font=("Arial", 15)).grid(row=i, column=1, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{prix_achat:.2f} $", font=("Arial", 15)).grid(row=i, column=2, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{prix_actuel:.2f} $", font=("Arial", 15)).grid(row=i, column=3, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{pourcentage:+.2f} %", font=("Arial", 15),
                         text_color=couleur).grid(row=i, column=4, padx=10, pady=5)

            bouton_vendre = ctk.CTkButton(
                self, text="Vendre", fg_color="transparent", hover_color="red",
                font=("Arial", 15), command=lambda a=nom: self.vendre_action(a)
            )
            bouton_vendre.grid(row=i, column=5, padx=0, pady=5)

            i += 1

        # Nettoie les actions à 0 dans self.actions + JSON
        if actions_a_supprimer:
            for nom in actions_a_supprimer:
                if nom in self.actions:
                    del self.actions[nom]
                if self.user and self.user.stocks_owned and nom in self.user.stocks_owned:
                    del self.user.stocks_owned[nom]

            # Sauvegarde du JSON
            if self.user:
                self.user.stocks_owned = {
                    nom: {"prix_achat": info["prix_achat"], "quantite": info["quantite"]}
                    for nom, info in self.actions.items()
                }
                self.user.save_to_json()

     
        self.update_affichage()


    def update_affichage(self):
        if not self.stocks:
            return

        if self.temps == len(self.stocks[next(iter(self.stocks))]['Close']):
            self.temps = 1
        else:
           
            for widget in self.winfo_children():
                info = widget.grid_info()
                col = info.get("column")
                row = info.get("row")
                if (col in (3, 4) and row >= 2) or (row == 0 and col == 4):
                    widget.destroy()

            i = 2
            for nom, info in self.actions.items():
                prix_achat = float(info["prix_achat"])
                quantite = info["quantite"]

                self.ensure_data_for_action(nom, info)
                if info["data"] is None:
                    continue

                df_close = info["data"]["Close"]

                t = int(self.temps)
                if t < len(df_close):
                    prix_actuel = round(float(df_close.iloc[t]), 2)
                else:
                    prix_actuel = round(float(df_close.iloc[-1]), 2)

                pourcentage = round(((prix_actuel - prix_achat) / prix_achat) * 100, 2) if prix_achat != 0 else 0.0
                couleur = "green" if pourcentage >= 0 else "red"

                ctk.CTkLabel(self, text=nom, font=("Arial", 20, "bold")).grid(row=i, column=0, padx=10, pady=5)
                ctk.CTkLabel(self, text=f"{quantite}", font=("Arial", 15)).grid(row=i, column=1, padx=10, pady=5)
                ctk.CTkLabel(self, text=f"{prix_achat:.2f} $", font=("Arial", 15)).grid(row=i, column=2, padx=10, pady=5)
                ctk.CTkLabel(self, text=f"{prix_actuel:.2f} $", font=("Arial", 15)).grid(row=i, column=3, padx=10, pady=5)
                ctk.CTkLabel(self, text=f"{pourcentage:+.2f} %", font=("Arial", 15),
                             text_color=couleur).grid(row=i, column=4, padx=10, pady=5)

                i += 1

            # Date et argent
            premier_stock = next(iter(self.stocks))
            date = self.stocks[premier_stock].index[self.temps].date()
            self.date = ctk.CTkLabel(self, text=date, text_color="light gray", font=("Arial", 24))
            self.date.grid(row=0, column=4, padx=(0, 10), pady=(10, 10))

            self.argent_label.configure(text=f"{self.argent:.2f} $")

            self.temps += 1
            self.boucle_id = self.after(5000, lambda: self.update_affichage())

  
    def clear_main_frame(self):
        if hasattr(self, "boucle_id"):
            try:
                self.after_cancel(self.boucle_id)
            except Exception:
                pass

        for widget in self.winfo_children():
            widget.destroy()


    def vendre_action(self, action):
        if action not in self.actions:
            return

        info = self.actions[action]
        self.ensure_data_for_action(action, info)
        if info["data"] is None:
            return

        df_close = info["data"]["Close"]

        if self.temps < len(df_close):
            prix_actuel = float(df_close.iloc[self.temps])
        else:
            prix_actuel = float(df_close.iloc[-1])

        # Met à jour l'argent
        self.argent += prix_actuel
        if self.user:
            self.user.balance = self.argent
            self.user.change_balance(self.argent)

        # Diminue la quantité
        info["quantite"] -= 1
        if info["quantite"] <= 0:
            del self.actions[action]

        # Met à jour user.stocks_owned 
        if self.user:
            self.user.stocks_owned = {
                nom: {"prix_achat": d["prix_achat"], "quantite": d["quantite"]}
                for nom, d in self.actions.items()
                if d["quantite"] > 0
            }
            self.user.save_to_json()

        # Réafficher le tableau
        for widget in self.winfo_children():
            info_w = widget.grid_info()
            row = info_w.get("row", 0)
            if row >= 2:
                widget.destroy()

        i = 2
        for nom, d in self.actions.items():
            prix_achat = float(d["prix_achat"])
            quantite = d["quantite"]

            self.ensure_data_for_action(nom, d)
            if d["data"] is None:
                continue

            df_close = d["data"]["Close"]
            if self.temps < len(df_close):
                prix_actuel = round(float(df_close.iloc[self.temps]), 2)
            else:
                prix_actuel = round(float(df_close.iloc[-1]), 2)

            pourcentage = round(((prix_actuel - prix_achat) / prix_achat) * 100, 2) if prix_achat != 0 else 0.0
            couleur = "green" if pourcentage >= 0 else "red"

            ctk.CTkLabel(self, text=nom, font=("Arial", 20, "bold")).grid(row=i, column=0, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{quantite}", font=("Arial", 15)).grid(row=i, column=1, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{prix_achat:.2f} $", font=("Arial", 15)).grid(row=i, column=2, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{prix_actuel:.2f} $", font=("Arial", 15)).grid(row=i, column=3, padx=10, pady=5)
            ctk.CTkLabel(self, text=f"{pourcentage:+.2f} %", font=("Arial", 15),text_color=couleur).grid(row=i, column=4, padx=10, pady=5)

            bouton_vendre = ctk.CTkButton( self, text="Vendre", fg_color="transparent", hover_color="red", font=("Arial", 15), command=lambda a=nom: self.vendre_action(a))
            bouton_vendre.grid(row=i, column=5, padx=0, pady=5)

            i += 1

        self.argent_label.configure(text=f"{self.argent:.2f} $")


    def retour(self):
        from watchlist import Watchlist
        self.clear_main_frame()
        Watchlist(master=self.master, stocks=self.stocks,temps=self.temps, compte=self, user=self.user, watchlist=self.watchlist)
