import customtkinter as ctk
import yfinance as yf
from watchlist import Watchlist  
import json
import os
from user import User


class LoginPage(ctk.CTkFrame):
    def __init__(self, master= None, stocks =None):
   
        super().__init__(master)
        self.master = master
        self.stocks = stocks

       # fenêtre principale qui s'adapte
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        # conteneur vertical centré
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="nsew")

        # centrage vertical/horizontal 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

     
        form = ctk.CTkFrame(container, fg_color="transparent")
        form.grid(row=0, column=0, padx=40, pady=60)  

        # titre
        title = ctk.CTkLabel(form, text="Connexion", font=("Arial", 28, "bold"))
        title.grid(row=0, column=0, pady=(5, 15))

   
        self.username_entry = ctk.CTkEntry(form, placeholder_text="Nom d'utilisateur", width=250, height=35)
        self.username_entry.grid(row=1, column=0, padx=10, pady=6)

        self.password_entry = ctk.CTkEntry(form, placeholder_text="Mot de passe", show="*", width=250, height=35)
        self.password_entry.grid(row=2, column=0, padx=10, pady=6)

    
        self.message_label = ctk.CTkLabel(form, text="", text_color="red", font=("Arial", 13))
        self.message_label.grid(row=3, column=0, pady=(4, 6))


        self.login_button = ctk.CTkButton(form, text="Se connecter", width=200, height=35, command=self.attempt_login)
        self.login_button.grid(row=4, column=0, pady=(8, 4))

      
        self.create_button = ctk.CTkButton(form, text="Créer un compte", width=200, height=35, command=self.create_account)
        self.create_button.grid(row=5, column=0, pady=(2, 10))


    def attempt_login(self):

        # Récuère le nom d'utilisateur et le mot de passe dans les entry
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        usersInfo_file = "users.json"

        if not os.path.exists(usersInfo_file):
            self.message_label.configure(text="Aucun compte n'existe encore.", text_color="red")
            return

        with open(usersInfo_file, "r") as f:
            users = json.load(f)

            user_found = None
            self.stocks = {}

            for user in users :  # regarde si l'utilisateur et le mot de passe correspond a un utilisateur dans le json
                if user["username"] == username and user["password"] == password :
                    user_found = user # si l'utilisateur est trouvé on garde ses infos pour les utiliser plus bas
                    break

            if user_found is None : 
                self.message_label.configure(text="Identifiants incorrects.", text_color="red")

            else :
                self.message_label.configure(text="Connexion réussie!", text_color="green")
                self.clear_main_frame()
                
                current_user = User (
                    username= user_found["username"],
                    password= user_found["password"],
                    balance= user_found["balance"],
                    stocks_owned= user_found["stocks_owned"])
                
                for stock in current_user.stocks_owned :
                    self.stocks[stock] = yf.download(stock, start="2024-01-01", end="2025-10-11", interval="1d")
                    
                from watchlist import Watchlist
                self.watchlist_page =  Watchlist(master=self.master, stocks=self.stocks, temps=0, compte= None, user = current_user) # ouvre la page principale Watchlist
                
              


    def clear_main_frame(self):
            for widget in self.master.winfo_children():
                widget.destroy()
       
    def create_account(self):

        # Récupère les infos entrées
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        # Vérifie que les deux champs sont remplis
        if not username or not password:
            self.message_label.configure(text="Veuillez remplir tous les champs.", text_color="red")
            return

        usersInfo_file = "users.json"

        if os.path.exists(usersInfo_file): # si le fichier existe on le charge
            with open(usersInfo_file, "r") as f:
                users = json.load(f)
        else : # si aucun fichier on crée une liste vide pour la création d'un fichier 
            users = []


        for user in users :
            if user["username"] == username :
                self.message_label.configure(text="Ce nom d'utilisateur existe déjà.", text_color="red")
                return
        
        new_user = {
        "username": username,
        "password": password,
        "balance": 1000,
        "stocks_owned": []
        }
    
        # Ajoute nouveau compte liste
        users.append(new_user)
        
        # Sauvegarde fichier avec nouveau compte
        with open(usersInfo_file, "w") as f:
            json.dump(users, f)

        self.message_label.configure(text="Compte créé avec succès!", text_color="green")