import customtkinter as ctk

class Acheter(ctk.CTkFrame) :
    def __init__(self, master = None, stocks = None, temps = None, action = None, argent = None, user=None, compte = None, watchlist = None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.action = action if action is not None else {}
        self.temps = temps
        self.argent = float(argent)
        self.user = user
        self.compte = compte
        self.watchlist = watchlist
        self.create_widgets()  
        

    def create_widgets(self):
        
         # Configuration principale
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.titre_label = ctk.CTkLabel(self, text=f"Acheter : {self.action}", font=("Arial", 28, "bold"))
        self.titre_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        self.retour_button = ctk.CTkButton(self, text="⬅ Retour", fg_color="transparent", hover_color="cyan", font=("Arial", 28, "bold"), command=self.retour)
        self.retour_button.grid(row=0, column=2, padx=(20, 10), sticky="e")

        # affiche prix actuel de l'action
        current_price = round(float(self.stocks[self.action]["Close"].iloc[self.temps]), 2)
        self.prix_label = ctk.CTkLabel(self, text=f"Prix actuel : {current_price:.2f} $", font=("Arial", 22))
        self.prix_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # affiche le solde du compte de l'utilisateur
        self.balance_label = ctk.CTkLabel(self, text=f"Votre solde : {self.user.balance:.2f} $", font=("Arial", 18))
        self.balance_label.grid(row=2, column=0, columnspan=2, pady=(0, 20))


        # Sélection de quantité
        self.quantite_label = ctk.CTkLabel(self, text="Quantité :", font=("Arial", 18))
        self.quantite_label.grid(row=3, column=0, sticky="w", padx=10)

        self.quantite_entry = ctk.CTkEntry(self, placeholder_text="Entrez la quantité", width=150)
        self.quantite_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w") 

        self.acheter_action_button = ctk.CTkButton(self,text= f"Acheter des actions de {self.action}", width=200, height=35, command= lambda a = self.action :self.acheter_action(a))
        self.acheter_action_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # message erreur ou validation
        self.message_label = ctk.CTkLabel(self,text="", text_color="red", font=("Arial", 13))
        self.message_label.grid(row=3, column=0, pady=(4, 6))



    def clear_main_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

 
    def retour(self):
        from watchlist import Watchlist
        self.clear_main_frame()
        Watchlist(master=self.master, stocks=self.stocks,temps=self.temps,compte=self.compte,user=self.user, watchlist= self.watchlist) 

       
    def acheter_action(self, action):

        prix_achat = round(float(self.stocks[action]["Close"].iloc[self.temps - 1]), 2)
        quantite = int(self.quantite_entry.get().strip())

        if quantite <= 0:
            self.message_label.configure(text="Quantité invalide.", text_color="red")
            return

        if self.compte is None:
            from compte import Compte
            self.compte = Compte(self.master, self.stocks, self.temps,
                                action={}, argent=self.user.balance, user=self.user)

        self.compte.argent = self.user.balance
        cout_total = prix_achat * quantite

        if self.compte.argent < cout_total:
            self.message_label.configure(text="Pas assez de fond pour acheter cette action !", text_color="red")
            return

        # Déduire l'argent
        self.compte.argent -= cout_total
        self.user.balance -= cout_total

        # Mise à jour du compte (self.compte.actions)
        if action in self.compte.actions:
            ancienne_quantite = self.compte.actions[action]["quantite"]
            ancien_prix = self.compte.actions[action]["prix_achat"]

            nouveau_prix_moyen = (
                (ancien_prix * ancienne_quantite) + (prix_achat * quantite)
            ) / (ancienne_quantite + quantite)

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

            nouveau_prix_moyen = (
                (ancien_prix * ancienne_quantite) + (prix_achat * quantite)
            ) / (ancienne_quantite + quantite)

            self.user.stocks_owned[action]["prix_achat"] = nouveau_prix_moyen
            self.user.stocks_owned[action]["quantite"] += quantite
        else:
            self.user.stocks_owned[action] = {
                "prix_achat": prix_achat,
                "quantite": quantite
            }

        # Sauvegarder le nouveau solde (et stocks_owned) dans le JSON
        self.user.change_balance(self.compte.argent)
