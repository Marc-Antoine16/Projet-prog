import customtkinter as ctk
import json

class AdminPage(ctk.CTkFrame):
    def __init__(self, master=None, stocks = None, temps = None, compte = None, users = None, watchlist = None):
        super().__init__(master)
        self.master = master
        self.users = users
        self.stocks = stocks
        self.temps = temps
        self.compte = compte
        self.watchlist = watchlist

        self.create_widgets()

    def create_widgets(self):

        self.grid(row=0, column=0, sticky="nsew")

        # Configuration du layout pour sidebar + contenu
        self.grid_columnconfigure(0, weight=0)   # sidebar
        self.grid_columnconfigure(1, weight=1)   # contenu
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color="#1A1A1A", width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        ctk.CTkLabel(self.sidebar, text="Admin Panel", font=("Arial", 24, "bold")).pack(pady=20)

     
        self.btn_users = ctk.CTkButton(self.sidebar, text="👤 Utilisateurs", command=  self.show_users)
        self.btn_users.pack(fill="x", pady=10)

        self.btn_actions = ctk.CTkButton(self.sidebar, text="📈 Actions détenues", command=  self.show_actions)
        self.btn_actions.pack(fill="x", pady=10)

        self.btn_watchlist = ctk.CTkButton(self.sidebar, text="Watchlist", command= self.show_watchlist)
        self.btn_watchlist.pack(fill="x", pady=10)

        ctk.CTkButton(self.sidebar, text="Déconnexion", fg_color="red",hover_color="#AA0000", command=self.logout).pack(fill="x", pady=40)

        # contenu 
        self.content = ctk.CTkFrame(self, fg_color="#2E2E2E")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)


        title = ctk.CTkLabel(self.content,text="Panneau Administrateur",font=("Arial", 28, "bold"))
        title.grid(row=0, column=0, pady=40)

        self.show_users_section()


    def show_users_section(self):

        self.clear_content()

        title = ctk.CTkLabel(self.content, text="Gestion des utilisateurs",font=("Arial", 28, "bold"))
        title.pack(pady=20)

        # Liste des utilisateurs
        usernames = [u["username"] for u in self.users if u["role"] != "admin"]
        self.user_select = ctk.CTkComboBox(self.content, values=usernames)
        self.user_select.pack(pady=10)

        ctk.CTkButton(self.content, text="Charger utilisateur", command=self.load_user).pack(pady=10)

        self.user_info = ctk.CTkLabel(self.content, text="", font=("Arial", 18))
        self.user_info.pack(pady=10)

        # Modifier solde
        self.new_balance_entry = ctk.CTkEntry(self.content, placeholder_text="Nouveau solde")
        self.new_balance_entry.pack(pady=5)

        ctk.CTkButton(self.content, text="Modifier solde",command=self.update_balance).pack(pady=5)

        # Modifier mot de passe
        self.new_pw_entry = ctk.CTkEntry(self.content, placeholder_text="Nouveau mot de passe")
        self.new_pw_entry.pack(pady=5)

        ctk.CTkButton(self.content, text="Changer mot de passe",command=self.update_password).pack(pady=5)

        # Reset user
        ctk.CTkButton(self.content, text="Réinitialiser le compte",fg_color="orange",command=self.reset_user).pack(pady=20)

        # Supprimer user
        ctk.CTkButton(self.content, text="Supprimer l'utilisateur",fg_color="red",command=self.delete_user).pack(pady=10)
        
 
    
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
                    watchlist=user["watchlist"]
                )
                break

        self.user_info.configure(text=f"Utilisateur chargé : {self.current_user.username}\n"f"Solde actuel : {self.current_user.balance:.2f} $",text_color="white")

    def update_balance(self):
         
        if not hasattr(self, "current_user"):
            self.user_info.configure(text=" Aucun utilisateur sélectionné.", text_color="red")
            return
        new_balance = float(self.new_balance_entry.get())
        self.current_user.change_balance(new_balance)
        self.user_info.configure(text=f"Solde mis à jour : {new_balance}$", text_color="green")

      
    def logout(self):
            self.clear_main_frame()
            from login import LoginPage
            LoginPage(master=self.master, stocks=self.stocks)

    def show_watchlist(self):
        if not hasattr(self, "current_user"):
            self.user_info.configure(text=" Aucun utilisateur sélectionné.", text_color="red")
            return

        self.clear_content()

        title = ctk.CTkLabel(self.content, text=f"Watchlist de {self.current_user.username}", font=("Arial", 26, "bold"))
        title.pack(pady=20)

        self.watchlist_message = ctk.CTkLabel(self.content, text="", font=("Arial", 16))
        self.watchlist_message.pack(pady=5)

    

        # Liste actuelle
        if not self.current_user.watchlist:
            ctk.CTkLabel(self.content, text="Aucune action dans la watchlist.", text_color="gray").pack(pady=10)
        else:
            for stock in self.current_user.watchlist:
                frame = ctk.CTkFrame(self.content, fg_color="#3A3A3A")
                frame.pack(pady=5, fill="x", padx=30)
                ctk.CTkLabel(frame, text=stock, font=("Arial", 18)).pack(side="left", padx=10)
                ctk.CTkButton(frame, text="Supprimer", fg_color="red", command=lambda s=stock: self.remove_from_watchlist(s)).pack(side="right", padx=10)

        # Ajouter une action
        ctk.CTkLabel(self.content, text="Ajouter une action :", font=("Arial", 16)).pack(pady=10)
        self.new_stock_entry = ctk.CTkEntry(self.content, placeholder_text="Symbole ex: AAPL")
        self.new_stock_entry.pack(pady=5)
        ctk.CTkButton(self.content, text="Ajouter", command=self.add_to_watchlist).pack(pady=5)

    def update_password(self):

        if not hasattr(self, "current_user"):
            self.user_info.configure(text=" Aucun utilisateur sélectionné.", text_color="red")
            return
        
        new_password = self.new_pw_entry.get()
        
        if len(new_password) == 0:
            self.user_info.configure(text=" Mot de passe invalide ! ", text_color="red")
        elif new_password == self.current_user.password :
            self.user_info.configure(text=" Veuillez choisir un mot de passe différent ! ", text_color="red")
        else : 
            self.current_user.change_password(new_password)
            self.user_info.configure(text=f"Mot de passe mis à jour : {new_password} ", text_color="green")

    def reset_user(self):

        self.current_user.change_balance(1000)
        self.current_user.change_stocks_owned({})
        self.current_user.change_watchlist([])
        self.current_user.save_to_json()
        self.user_info.configure(text="Compte réinitialisé ", text_color="green")


    def delete_user(self):

        from tkinter import messagebox

        # Vérifie qu'un utilisateur est chargé
        if not hasattr(self, "current_user"):
            self.user_info.configure(text=" Aucun utilisateur sélectionné.", text_color="red")
            return

        # Confirmation avant suppression
        confirm = messagebox.askyesno("Confirmation", f"Supprimer {self.current_user.username} ?")
        if not confirm:
            return

        # Supprime du fichier JSON
        with open("users.json", "r") as f:
            users = json.load(f)

        new_users = []
        for user in users:
            if user["username"] != self.current_user.username:
                new_users.append(user)

        with open("users.json", "w") as f:
            json.dump(new_users, f, indent=4)

        # Met à jour la liste déroulante
        updated_usernames = []
        for user in new_users:
            if user["role"] != "admin":
                updated_usernames.append(user["username"])

        self.user_select.configure(values=updated_usernames)

        # Message de confirmation
        self.user_info.configure(text=f" Utilisateur {self.current_user.username} supprimé avec succès.",text_color="green")
        self.current_user = None


    def show_users(self):
        self.clear_content()
        self.show_users_section()

    def show_actions(self):
        print("Watchlist")

    def clear_main_frame(self):
        if hasattr(self, "boucle_id"):
            try:
                self.after_cancel(self.boucle_id)
            except Exception:
                pass

        for widget in self.winfo_children():
            widget.destroy()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

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
        
    def add_to_watchlist(self):
        import yfinance as yf
        stock = self.new_stock_entry.get().strip().upper()

       
        if not stock:
            self.watchlist_message.configure(text=" Entrez un symbole valide.", text_color="red")
            return

        # Vérifie si l'action est déjà dans la watchlist
        if stock in self.current_user.watchlist:
            self.watchlist_message.configure(text=" Cette action est déjà dans la watchlist.", text_color="orange")
            return

        # Vérifie si l'action existe via yfinance
        try:
            df = yf.download(stock, start="2024-01-01", end="2025-10-11", interval="1d")
            df["Close"] = df["Close"].astype(float)
            self.stocks[stock] = df
        except Exception as e:
            print(f"Veuillez choisir un stock valide !{stock} :", e)
            return

        # Si tout est bon, ajoute à la watchlist
        self.current_user.add_to_watchlist(stock)
        self.watchlist_message.configure(text=f"✅ {stock} ajouté à la watchlist.", text_color="green")

        # Rafraîchit l'affichage
        self.clear_content()
        self.show_watchlist()
    def option_changed(self, value): #ajout nouveau stock, créer widgets sans reconstruire la page pour que les labels de rendement deja existant reste visible et continue de se mettre a jour
        if value == "Ajouter...":
            return
        
        if value in self.stocks:  # déjà dans la watchlist
            return
        
        try:
            df = yf.download(value, start="2024-01-01", end="2025-10-11", interval="1d")
            df["Close"] = df["Close"].astype(float)
            self.stocks[value] = df
        except Exception as e:
            print(f"Erreur téléchargement du stock {value} :", e)
            return

        
        self.user.add_to_watchlist(value)