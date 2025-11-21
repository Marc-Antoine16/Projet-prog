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
        username = self.user_select.get()

        for user in self.users:
            if user["username"] == username:
                self.current_user = user
                break

        self.user_info.configure(text=f"Utilisateur chargé : {self.current_user['username']}\n" f"Solde actuel : {self.current_user['balance']:.2f} $",text_color="white")

    def update_balance(self):
        if not hasattr(self, "current_user"):
            return

        try:
            new_balance = float(self.balance_entry.get().strip())
        except:
            self.message.configure(text="Solde invalide", text_color="red")
            return

        self.current_user["balance"] = new_balance

        # Sauvegarde dans le JSON
        with open("users.json", "w") as f:
            json.dump(self.users, f, indent=4)


        self.user_info.configure(text= f"Solde mis à jour \n" f"Solde actuel : {new_balance:.2f} $",text_color="green")

      
    def logout(self):
            self.clear_main_frame()
            from login import LoginPage
            LoginPage(master=self.master, stocks=self.stocks)

    def show_watchlist(self):
        print("Watchlist")

    def update_password(self):
        print("Watchlist")

    def reset_user(self):
        print("Watchlist")

    def delete_user(self):
            print("Watchlist")

    def show_users(self):
        print("Watchlist")
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