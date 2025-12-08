import customtkinter as ctk

class Acheter(ctk.CTkFrame) :
    def __init__(self, master = None, stocks = None, temps = None, action = None, argent = None, user=None, compte = None, watchlist = None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.action = action
        self.temps = temps
        self.argent = float(argent)
        self.user = user
        self.compte = compte
        self.watchlist = watchlist

        self.df = self.stocks[self.action]

        self.create_widgets()
     

    def create_widgets(self):

        # Configuration de la grille
        for i in range(12):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

        self.grid(row=0, column=0, sticky="nsew")

        # Titre et bouton retour
        titre = ctk.CTkLabel(self, text=f"Achat : {self.action}", font=("Arial", 32, "bold"))
        titre.grid(row=0, column=0, columnspan=6, pady=(20, 10))

        retour = ctk.CTkButton(self, text="⬅ Retour", fg_color="transparent",hover_color="cyan",font=("Arial", 22, "bold"),command=self.retour)
        retour.grid(row=0, column=10, columnspan=2, padx=20)

        # Info et prix
        current_price = round(float(self.df["Close"].iloc[self.temps]), 2)
        yesterday = float(self.df["Close"].iloc[self.temps - 1])
        change = current_price - yesterday
        pct = (change / yesterday) * 100 if yesterday != 0 else 0 

        couleur = "green" if change >= 0 else "red"
        signe = "+" if change >= 0 else "-"

        # cadre infos
        info = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=12)
        info.grid(row=1, column=0, columnspan=6, rowspan=3, padx=20, pady=10, sticky="nsew")

        ctk.CTkLabel(info, text=f"Prix actuel : {current_price:.2f} $", font=("Arial", 26, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(info,text=f"{signe}{abs(change):.2f} $  ({signe}{abs(pct):.2f} %)",text_color=couleur,font=("Arial", 22, "bold")).grid(row=1, column=0, sticky="w", padx=10)

        high = round(float(self.df["High"].iloc[self.temps]), 2)
        low = round(float(self.df["Low"].iloc[self.temps]), 2)
        volume = int(self.df["Volume"].iloc[self.temps])

        stats = ctk.CTkFrame(info, fg_color="transparent")
        stats.grid(row=2, column=0, sticky="w", padx=10, pady=10)

        ctk.CTkLabel(stats, text=f"Plus haut du jour : {high} $", font=("Arial", 18)).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(stats, text=f"Plus bas du jour : {low} $", font=("Arial", 18)).grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(stats, text=f"Volume : {volume:,}", font=("Arial", 18)).grid(row=2, column=0, sticky="w")

        
        solde = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=12)
        solde.grid(row=1, column=7, columnspan=4, rowspan=1, padx=20, pady=10, sticky="nsew")

        ctk.CTkLabel(solde, text=f"Votre solde : {self.user.balance:.2f} $", font=("Arial", 22, "bold")).grid(row=0, column=0, pady=10, padx=10)

        # Quantité et coût total
        achat = ctk.CTkFrame(self, fg_color="#1a1a1a", corner_radius=12)
        achat.grid(row=5, column=0, columnspan=10, rowspan=4, padx=20, pady=10, sticky="nsew")

        ctk.CTkLabel(achat, text="Quantité :", font=("Arial", 20)).grid(row=0, column=0, padx=20, pady=20)

        self.quantite_entry = ctk.CTkEntry(achat, width=120, placeholder_text="Ex: 5")
        self.quantite_entry.grid(row=0, column=1, padx=10, pady=20)

        self.quantite_entry.bind("<KeyRelease>", lambda e: self.update_cost())

        self.cout_label = ctk.CTkLabel(achat, text="Coût total : 0.00 $", font=("Arial", 20))
        self.cout_label.grid(row=1, column=0, columnspan=3, pady=10)

        self.restant_label = ctk.CTkLabel(achat, text="", font=("Arial", 20))
        self.restant_label.grid(row=2, column=0, columnspan=3, pady=10)

        bouton = ctk.CTkButton(achat, text=f"Acheter {self.action}",font=("Arial", 24, "bold"),hover_color="green",command=lambda: self.acheter_action(self.action))
        bouton.grid(row=3, column=0, columnspan=3, pady=20)

        # Message d’erreur
        self.message_label = ctk.CTkLabel(self, text="", text_color="red", font=("Arial", 18))
        self.message_label.grid(row=10, column=0, columnspan=10)

    # Mise à jour du coût total et du solde restant
    def update_cost(self):
            txt = self.quantite_entry.get().strip() # Récupère le texte entré
            if not txt.isdigit(): # Vérifie si c'est un entier positif
                self.cout_label.configure(text="Coût total : -") 
                self.restant_label.configure(text="")
                return

            q = int(txt)
            price = round(float(self.df["Close"].iloc[self.temps]), 2) 
            total = q * price

            self.cout_label.configure(text=f"Coût total : {total:.2f} $")

            restant = self.user.balance - total
            couleur = "green" if restant >= 0 else "red"

            self.restant_label.configure(
                text=f"Solde après achat : {restant:.2f} $",
                text_color=couleur
        )

    # Nettoyage du frame principal
    def clear_main_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

   #  Retour à la watchlist
    def retour(self):
        from watchlist import Watchlist
        self.clear_main_frame()
        Watchlist(master=self.master, stocks=self.stocks,temps=self.temps,compte=self.compte,user=self.user, watchlist= self.watchlist) 

     # Logique d'achat d'une action  
    def acheter_action(self, action):

        prix_achat = round(float(self.stocks[action]["Close"].iloc[self.temps - 1]), 2)
        quantite = int(self.quantite_entry.get().strip())

        # Validation de la quantité
        if quantite <= 0:
            self.message_label.configure(text="Quantité invalide.", text_color="red")
            return

        # Initialisation du compte si nécessaire
        if self.compte is None:
            from compte import Compte
            self.compte = Compte(self.master, self.stocks, self.temps,action={}, argent=self.user.balance, user=self.user)

        self.compte.argent = self.user.balance
        cout_total = prix_achat * quantite

        # Vérification des fonds suffisants
        if self.compte.argent < cout_total:
            self.message_label.configure(text="Pas assez de fond pour acheter cette action !", text_color="red")
            return

        # Déduire l'argent
        self.compte.argent -= cout_total
        self.user.balance -= cout_total

        # Mise à jour du compte
        if action in self.compte.actions:
            ancienne_quantite = self.compte.actions[action]["quantite"]
            ancien_prix = self.compte.actions[action]["prix_achat"]

            nouveau_prix_moyen = ((ancien_prix * ancienne_quantite) + (prix_achat * quantite) ) / (ancienne_quantite + quantite)

            self.compte.actions[action]["prix_achat"] = nouveau_prix_moyen
            self.compte.actions[action]["quantite"] += quantite

        else:
            # Première fois que cette action est dans le compte
            self.compte.actions[action] = {
                "data": self.stocks[action],   # DataFrame en mémoire seulement
                "prix_achat": prix_achat,
                "quantite": quantite
            }

        # Mise à jour du user 
        if action in self.user.stocks_owned:
            ancienne_quantite = self.user.stocks_owned[action]["quantite"]
            ancien_prix = self.user.stocks_owned[action]["prix_achat"]

            nouveau_prix_moyen = ((ancien_prix * ancienne_quantite) + (prix_achat * quantite)) / (ancienne_quantite + quantite)

            self.user.stocks_owned[action]["prix_achat"] = nouveau_prix_moyen
            self.user.stocks_owned[action]["quantite"] += quantite
        else:
            self.user.stocks_owned[action] = {
                "prix_achat": prix_achat,
                "quantite": quantite
            }

        # Sauvegarder le nouveau solde (et stocks_owned) dans le JSON
        self.user.change_balance(self.compte.argent)
