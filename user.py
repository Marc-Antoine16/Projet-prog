import os
import json

class User :
    def __init__(self, username, password, balance, role, stocks_owned = None, watchlist=None):
        
        self.username = username
        self.password = password
        self.balance = balance
        self.role = role
        self.stocks_owned = stocks_owned if stocks_owned is not None else {} # si il existe une liste la prendre sinon la crée
        self.watchlist = watchlist if watchlist is not None else [] # si il existe une liste la prendre sinon la crée


    # Ajout d'une action possédée
    def add_stock(self, stock, prix_achat=0, quantite=0) :
        # Ajouter une action possédée ou mettre à jour la quantité et le prix moyen d'achat
    
        if stock not in self.stocks_owned: # Si l'action n'est pas déjà possédée, l'ajouter
            self.stocks_owned[stock] = { "prix_achat": prix_achat,  "quantite": quantite}
            
            ancienne_quantite = self.stocks_owned[stock]["quantite"]
            ancien_prix = self.stocks_owned[stock]["prix_achat"]

           
            if quantite > 0: # Éviter la division par zéro
                nouveau_prix_moyen = ((ancien_prix * ancienne_quantite) + (prix_achat * quantite)) / (ancienne_quantite + quantite)
                self.stocks_owned[stock]["prix_achat"] = nouveau_prix_moyen
                self.stocks_owned[stock]["quantite"] += quantite

    
        self.save_to_json() # Sauvegarder les modifications dans le fichier JSON

    # Gérer le transfert d'une action à un autre utilisateur
    def gerer_transfert(self, nom_stock, destinataire, emetteur) :
        with open("users.json", "r") as f:
            users = json.load(f)

        for user in users :
            if user["username"] == destinataire :
                user_destinataire = user # Trouver le destinataire
            if user["username"] == emetteur.username :
                user_emetteur = user # Trouver l'émetteur
                
        # Vérifier si l'émetteur possède l'action
        if nom_stock in user_emetteur["stocks_owned"] :
            quantite_possedee = user_emetteur["stocks_owned"][nom_stock]["quantite"]

            # Transférer une unité de l'action
            if quantite_possedee > 0 :
                # Décrémenter la quantité de l'émetteur
                user_emetteur["stocks_owned"][nom_stock]["quantite"] -= 1

                # Supprimer l'action si la quantité devient zéro
                if user_emetteur["stocks_owned"][nom_stock]["quantite"] == 0 :
                    del user_emetteur["stocks_owned"][nom_stock]

                # Incrémenter la quantité du destinataire
                if nom_stock in user_destinataire["stocks_owned"] :
                    user_destinataire["stocks_owned"][nom_stock]["quantite"] += 1
                else :
                    user_destinataire["stocks_owned"][nom_stock] = {
                        "prix_achat" : 0, # Prix d'achat inconnu lors du transfert
                        "quantite" : 1
                    }

                # Sauvegarder les modifications dans le fichier JSON
                with open("users.json", "w") as f:
                    json.dump(users, f, indent=4)
    
    
    # Suppression d'une action possédée
    def remove_stock(self, stock) :

        if stock in self.stocks_owned : 
            del self.stocks_owned[stock]
            self.save_to_json()
    
    def change_balance(self, amount) :
        self.balance = amount
        self.save_to_json()

    def change_password(self, password) :
            self.password = password
            self.save_to_json()


    # Modifier les actions possédées
    def change_stocks_owned(self, stocks_owned) :
        self.stocks_owned = stocks_owned
        self.save_to_json()

    # Modifier la watchlist
    def change_watchlist(self, watchlist) :
        self.watchlist = watchlist
        self.save_to_json()

    def add_to_watchlist(self, stock):
        if stock not in self.watchlist:
            self.watchlist.append(stock)
            self.save_to_json()

    def remove_from_watchlist(self, symbole):
        if symbole in self.watchlist:
            self.watchlist.remove(symbole)
            self.save_to_json()

    # Ajouter une action possédée ou mettre à jour la quantité et le prix moyen d'achat
    def add_owned_stock(self, symbole, prix_achat, quantite):
        if symbole not in self.stocks_owned: # Si l'action n'est pas déjà possédée, l'ajouter
            self.stocks_owned[symbole] = {"prix_achat": prix_achat,"quantite": quantite}
        else: # Mettre à jour le prix moyen d'achat et la quantité
            old_q = self.stocks_owned[symbole]["quantite"]
            old_p = self.stocks_owned[symbole]["prix_achat"]
            new_price = ((old_p * old_q) + (prix_achat * quantite)) / (old_q + quantite)
            self.stocks_owned[symbole]["prix_achat"] = new_price
            self.stocks_owned[symbole]["quantite"] += quantite

        self.save_to_json()

    def save_to_json(self, users_file="users.json"):
       
        if not os.path.exists(users_file): # Créer le fichier s'il n'existe pas
            return

        with open(users_file, "r") as f: # Lire les utilisateurs existants
            users = json.load(f)

        for user in users: # Mettre à jour les informations de l'utilisateur actuel
            if user["username"] == self.username:
                user["password"] = self.password
                user["balance"] = self.balance
                user["stocks_owned"] = self.stocks_owned
                user["watchlist"] = self.watchlist 

                break

        with open(users_file, "w") as f: # Écrire les modifications dans le fichier JSON
            json.dump(users, f, indent=4) # Sauvegarder avec une indentation pour la lisibilité