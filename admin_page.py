import customtkinter as ctk
import json
import pandas as pd
import yfinance as yf

class AdminPage(ctk.CTkFrame):
    def __init__(self, master=None, stocks=None, temps=None, compte=None, users=None, watchlist=None):
        super().__init__(master)
        self.master = master
        self.users = users
        self.stocks = stocks
        self.temps = temps
        self.compte = compte
        self.watchlist = watchlist 

        # Liste des stocks du S&P500 (pour ajout d'actions)
        self.options = pd.read_csv(
            "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
        )["Symbol"].tolist()
        self.options_with_placeholder = ["Ajouter action"] + self.options

        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, sticky="nsew")

        # Layout principal : sidebar + contenu
        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # contenu principal
        self.grid_rowconfigure(0, weight=1)

        # Sidebar 
        self.sidebar = ctk.CTkFrame(self, fg_color="#1A1A1A", width=220)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        title_label = ctk.CTkLabel(self.sidebar, text="Panneau admin", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, pady=(30, 40), padx=10)

        self.btn_users = ctk.CTkButton(self.sidebar, text="👤 Utilisateurs", command=self.show_users)
        self.btn_users.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.btn_actions = ctk.CTkButton(self.sidebar, text="📈 Actions détenues", command=self.show_actions)
        self.btn_actions.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        self.btn_watchlist = ctk.CTkButton(self.sidebar, text="📋 Watchlist", command=self.show_watchlist)
        self.btn_watchlist.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.btn_logout = ctk.CTkButton(self.sidebar, text="Déconnexion",fg_color="red",hover_color="#AA0000",command=self.logout,)
        self.btn_logout.grid(row=9, column=0, pady=(50, 10), padx=10, sticky="ew")

        # Contenu principal
        self.content = ctk.CTkFrame(self, fg_color="#2E2E2E")
        self.content.grid(row=0, column=1, sticky="nsew")

        # Configuration du grid pour le contenu
        for i in range(10):
            self.content.grid_columnconfigure(i, weight=1)

        self.show_users_section()

    # Section gestion des utilisateurs 
    def show_users_section(self):
        self.clear_content()

        # Titre centré
        title = ctk.CTkLabel(self.content, text="Gestion des utilisateurs", font=("Arial", 28, "bold"))
        title.grid(row=0, column=0, columnspan=10, pady=(60, 40), sticky="n")

        # Liste déroulente de nom !
        usernames = [user["username"] for user in self.users if user["role"] != "admin"]
        self.user_select = ctk.CTkComboBox(self.content, values=usernames)
        self.user_select.grid(row=1, column=5, pady=10, sticky="n")

        self.btn_charger_user = ctk.CTkButton(self.content, text="Charger utilisateur", command=self.load_user)
        self.btn_charger_user.grid(row=2, column=5, pady=10, sticky="n")

        self.user_info = ctk.CTkLabel(self.content, text="", font=("Arial", 18))
        self.user_info.grid(row=3, column=5, pady=10, sticky="n")

        self.new_balance_entry = ctk.CTkEntry(self.content, placeholder_text="Nouveau solde")
        self.new_balance_entry.grid(row=4, column=5, pady=5, sticky="n")

        self.btn_modifier_solde = ctk.CTkButton(self.content, text="Modifier solde", command=self.update_balance)
        self.btn_modifier_solde.grid(row=5, column=5, pady=5, sticky="n")

        self.new_pw_entry = ctk.CTkEntry(self.content, placeholder_text="Nouveau mot de passe")
        self.new_pw_entry.grid(row=6, column=5, pady=5, sticky="n")
        
        self.btn_modifier_mot_passe = ctk.CTkButton(self.content, text="Changer mot de passe", command=self.update_password)
        self.btn_modifier_mot_passe.grid(row=7, column=5, pady=5, sticky="n")

        self.btn_reset_user = ctk.CTkButton(self.content, text="Réinitialiser le compte", fg_color="orange", command=self.reset_user)
        self.btn_reset_user.grid(row=8, column=5, pady=10, sticky="n")

        self.btn_supprimer_user = ctk.CTkButton(self.content, text="Supprimer l'utilisateur", fg_color="red", command=self.delete_user)
        self.btn_supprimer_user.grid(row=9, column=5, pady=10, sticky="n")

    # Actions détenues
    def show_actions(self):
        if not hasattr(self, "current_user"):
            self.user_info.configure(text="Aucun utilisateur sélectionné.", text_color="red")
            return

        self.clear_content()

        # Titre 
        title = ctk.CTkLabel(self.content,text=f"Actions détenues par {self.current_user.username}",font=("Arial", 26, "bold"))
        title.grid(row=0, column=0, columnspan=10, pady=(50, 20), sticky="n")

        self.message_label = ctk.CTkLabel(self.content, text="", font=("Arial", 16))
        self.message_label.grid(row=1, column=0, columnspan=10, pady=(0, 20), sticky="n")
        if not self.current_user.stocks_owned:
            ctk.CTkLabel(self.content, text="Aucune action détenue actuellement.", text_color="gray").grid(row=1, column=5, pady=10)
            return

        # Pour chaque action détenue 
        for i, (symbol, data) in enumerate(self.current_user.stocks_owned.items(), start=2):
            frame = ctk.CTkFrame(self.content, fg_color="#3A3A3A", corner_radius=8)
            frame.grid(row=i, column=2, columnspan=6, pady=3, sticky="ew")

            # Ligne principale du cadre 
            info = f"{symbol} | Qté : {data['quantite']} | Prix moyen : {data['prix_achat']:.2f}$"
            ctk.CTkLabel(frame, text=info, font=("Arial", 16)).grid(row=0, column=0, padx=10, pady=5, sticky="w")

            # Sélecteur de destinataire pour le transfert
            usernames = [user["username"] for user in self.users if user["role"] != "admin" and user["username"] != self.current_user]
            self.transfer_select = ctk.CTkComboBox(frame, values=usernames)
            self.transfer_select.grid(row=0, column=1, pady=10, sticky="n")

            # Bouton de transfert
            self.transfer_btn = ctk.CTkButton(frame, text="Transfer", fg_color="green", command=lambda s= symbol, dest = self.transfer_select, sender = self.current_user : self.transfert(s,dest, sender))
            self.transfer_btn.grid(row=0, column=2, pady=10, sticky="n")



    # Transfert d'actions
    def transfert(self, nom_stock, nom_destinataire, mon_emetteur) : 

        destinataire = nom_destinataire.get().strip()
        stock = nom_stock
        self.current_user.gerer_transfert(stock, destinataire, mon_emetteur)

        self.clear_content()
        self.show_actions()


    def show_watchlist(self): # Affichage de la watchlist

        # Vérification utilisateur sélectionné
        if not hasattr(self, "current_user"):
            self.user_info.configure(text="Aucun utilisateur sélectionné.", text_color="red")
            return

        self.clear_content() 

        
        title = ctk.CTkLabel(self.content, text=f"Watchlist de {self.current_user.username}", font=("Arial", 26, "bold"))
        title.grid(row=0, column=0, columnspan=10, pady=(50, 20), sticky="n")

        # Message d'information sur la watchlist
        self.watchlist_message = ctk.CTkLabel(self.content, text="", font=("Arial", 16))
        self.watchlist_message.grid(row=2, column=5, pady=10, sticky="n")

        # Dropdown pour ajouter des actions
        self.dropdown = ctk.CTkOptionMenu(self.content, values=self.options_with_placeholder, command=self.option_changed)
        self.dropdown.set("Ajouter action")
        self.dropdown.grid(row=1, column=5, pady=10, sticky="n")

        # vérification watchlist vide
        if not self.current_user.watchlist:
            ctk.CTkLabel(self.content, text="Aucune action dans la watchlist.", text_color="gray").grid(row=3, column=5, pady=10)
            return
        # Affichage des actions dans la watchlist
        for i, stock in enumerate(self.current_user.watchlist, start=3):
            frame = ctk.CTkFrame(self.content, fg_color="#3A3A3A", corner_radius=8)
            frame.grid(row=i, column=2, columnspan=6, pady=3, sticky="ew")

            ctk.CTkLabel(frame, text=stock, font=("Arial", 18)).grid(row=0, column=0, padx=10, pady=5)
            ctk.CTkButton(frame, text="Supprimer", fg_color="red", command=lambda s=stock: self.remove_from_watchlist(s)).grid(row=0, column=1, padx=10, pady=5)

    # Chargement des données utilisateur
    def load_user(self):
        from user import User
        username = self.user_select.get()
        for user in self.users:
            if user["username"] == username:
                self.current_user = User(
                    username=user["username"],
                    password=user["password"],
                    balance=user["balance"],
                    role=user["role"],
                    stocks_owned=user["stocks_owned"],
                    watchlist=user["watchlist"],
                )
                break
        self.user_info.configure(text=f"Utilisateur chargé : {self.current_user.username}\nSolde actuel : {self.current_user.balance:.2f} $",text_color="white",)

    # Mise à jour du solde utilisateur
    def update_balance(self):
        
        if not hasattr(self, "current_user"):
            self.user_info.configure(text="Aucun utilisateur sélectionné.", text_color="red")
            return
        try:
            new_balance = float(self.new_balance_entry.get())
        except ValueError:
            self.user_info.configure(text="Entrée invalide.", text_color="red")
            return
        self.current_user.change_balance(new_balance)
        self.user_info.configure(text=f"Solde mis à jour : {new_balance}$", text_color="green")

    # Mise à jour du mot de passe utilisateur
    def update_password(self):
        if not hasattr(self, "current_user"):
            self.user_info.configure(text="Aucun utilisateur sélectionné.", text_color="red")
            return
        new_password = self.new_pw_entry.get()
        if len(new_password) == 0:
            self.user_info.configure(text="Mot de passe invalide !", text_color="red")
        elif new_password == self.current_user.password:
            self.user_info.configure(text="Veuillez choisir un mot de passe différent !", text_color="red")
        else:
            self.current_user.change_password(new_password)
            self.user_info.configure(text=f"Mot de passe mis à jour : {new_password}", text_color="green")

    # Réinitialisation du compte utilisateur
    def reset_user(self):
        self.current_user.change_balance(1000)
        self.current_user.change_stocks_owned({})
        self.current_user.change_watchlist([])
        self.current_user.save_to_json()
        self.user_info.configure(text="Compte réinitialisé", text_color="green")

    # Suppression de l'utilisateur
    def delete_user(self):
        from tkinter import messagebox
    
        if not hasattr(self, "current_user"):
            self.user_info.configure(text="Aucun utilisateur sélectionné.", text_color="red")
            return
        confirm = messagebox.askyesno("Confirmation", f"Supprimer {self.current_user.username} ?") # Demande de confirmation pour suppression
        if not confirm:
            return
        with open("users.json", "r") as f: # Lecture des utilisateurs dans le fichier JSON
            users = json.load(f) # chargement des données JSON
        
        new_users = [user for user in users if user["username"] != self.current_user.username] # Filtrage de l'utilisateur à supprimer

        with open("users.json", "w") as f: # Écriture des données mises à jour dans le fichier JSON
            json.dump(new_users, f, indent=4) # Sauvegarde des modifications
        updated_usernames = [user["username"] for user in new_users if user["role"] != "admin"]
        self.user_select.configure(values=updated_usernames)
        self.user_info.configure(text=f"Utilisateur {self.current_user.username} supprimé avec succès.", text_color="green")
        self.current_user = None

    # Affichage de la section utilisateurs
    def show_users(self):
        self.clear_content()
        self.show_users_section()

    # Déconnexion
    def logout(self):
        self.clear_main_frame()
        from login import LoginPage
        LoginPage(master=self.master, stocks=self.stocks)

    # Nettoyage du frame principal
    def clear_main_frame(self):
        if hasattr(self, "boucle_id"):
            try:
                self.after_cancel(self.boucle_id)
            except Exception:
                pass
        for widget in self.winfo_children():
            widget.destroy()

    # Nettoyage du contenu principal
    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # Suppression d'une action de la watchlist
    def remove_from_watchlist(self, stock):
        self.current_user.remove_from_watchlist(stock) 
        with open("users.json", "r") as f:
            users = json.load(f)
            for user in users:
                if user["username"] == self.current_user.username: 
                    self.current_user.watchlist = user["watchlist"]
                    break
        self.clear_content()
        self.show_watchlist()

    # Ajout d'une action à la watchlist
    def option_changed(self, value):
        if value == "Ajouter action":
            return
        if value in self.stocks:
            return
        try:
            df = yf.download(value, start="2024-01-01", end="2025-10-11", interval="1d")
            df["Close"] = df["Close"].astype(float)
            self.stocks[value] = df
        except Exception as e:
            print(f"Erreur téléchargement du stock {value} :", e)
            return
        self.current_user.add_to_watchlist(value)
        self.clear_content()
        self.show_watchlist()
