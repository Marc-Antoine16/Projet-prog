import customtkinter as ctk
from info import Info
import yfinance as yf
from graphe import Graph
from compte import Compte
import pandas as pd
import time
from PIL import Image
from datetime import date

class Watchlist(ctk.CTkFrame):
    def __init__(self, master=None, stocks=None, temps = None, compte = None, options=None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.temps = temps or 0
        self.compte = compte
        self.date = date.today()

        self.date_label = None

        if compte and compte.stocks is not None: #Si le compte existe, on prend sa watchlist  sinon, dict vide
            self.stocks = compte.stocks or {}
        else:
            self.stocks = {}

        if options is None: #Chargement de la liste des symboles S&P500
                try:
                    data = pd.read_csv("https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv")
                    self.options = data["Symbol"].dropna().tolist()
                except Exception as e:
                    print("Erreur lors du chargement du CSV :", e)
                    self.options = []
        else:
            self.options = options

        self.options_with_placeholder = ["Ajouter..."] + self.options
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.create_widgets()

    def create_widgets(self):
        self.master.grid_rowconfigure(0, weight= 1)
        self.master.grid_columnconfigure(0, weight= 1)

        # Le frame a plusieurs colonnes extensibles
        self.grid_rowconfigure((0, 1, 2,4,5,6,7,8,9,10), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5,6,7,8,9,10), weight=1)

        self.titre_label = ctk.CTkLabel(self, text="Watchlist", font=("Arial", 30, "bold"))
        self.titre_label.grid(row=0, column=1, pady=(10,10))

        self.dropdown = ctk.CTkOptionMenu(self,values=self.options_with_placeholder, command=self.option_changed)
        self.dropdown.set("Ajouter...")
        self.dropdown.grid(row=0, column=6, pady=(10,10))

        self.bouton_compte = ctk.CTkButton(self, text = "Compte", fg_color="transparent", hover_color="red", font=("Arial", 24), command = self.ouvrir_compte)
        self.bouton_compte.grid(row = 7, column = 0, pady = (10,10))

        self.btn_retour = ctk.CTkButton(self, text="Retour",fg_color="transparent",hover_color="light green",font=("Arial", 24, "bold"),command=self.aller_A_accueil)
        self.btn_retour.grid(row=0, column=0, pady=(0, 0))

        i = 1
        for stock in self.stocks:
            self.titre_action = ctk.CTkButton(self, text=stock ,fg_color = "transparent", hover_color="lightpink", font=("Arial", 24, "bold"), command=lambda s=stock: self.onButtonClicked(s))
            self.titre_action.grid(row=i, column=0, pady=(10,10))

            self.boutonGraphe = ctk.CTkButton(self, text="📈", fg_color="transparent", hover_color="orange", font=("Arial", 24), width=60, height=60 , command = lambda s = stock: self.ouvrir_graph(s))
            self.boutonGraphe.grid(row=i, column=9, pady=(10,10))
            
            self.bouton_supprime = ctk.CTkButton(self, text="❎", fg_color="transparent", hover_color="red", font=("Arial", 24), width=60, height=60, command = lambda s = stock: self.supprime_stock(s))
            self.bouton_supprime.grid(row=i, column=10, pady=(10,10))

            self.bouton_achat = ctk.CTkButton(self, text="Acheter", fg_color="transparent", hover_color="green", font=("Arial", 24), width=80, height=60 , command = lambda a = stock: self.acheter_stock(a))
            self.bouton_achat.grid(row = i, column = 4, pady = (10, 10))

            i += 1      

        self.boucle_stock()

    def boucle_stock(self):
        if not self.stocks:
            if self.date_label is not None:
                self.date_label.configure(text="Aucun stock")
            self.temps += 1  # le temps continue quand même
            self.boucle_id = self.after(5000, self.boucle_stock)
            return
        #Initialisation des dictionnaires de widgets si pas fait
        if not hasattr(self, "prix_buttons"):
            self.prix_buttons = {}
        if not hasattr(self, "rendement_labels"):
            self.rendement_labels = {}
        if not hasattr(self, "date_label"):
            self.date_label = None

        #Reset du temps si dépasse le nombre de jours
        if self.temps >= len(self.stocks[next(iter(self.stocks))]['Close']):
            self.temps = 0

        for i, stock in enumerate(self.stocks, start=1):
            data = self.stocks[stock]
            y = data["Close"]

            prix = round(float(y.iloc[self.temps].item()), 2)
            textePrix=str(prix) #evite le chargement

            if stock not in self.prix_buttons:
                self.prix_buttons[stock] = ctk.CTkButton(self,text=textePrix, fg_color="transparent", hover_color="lightpink",font=("Arial", 24, "bold"),command=lambda s=stock: self.onButtonClicked(s) )
                self.prix_buttons[stock].grid(row=i, column=1, pady=(10,10))
            else:
                self.prix_buttons[stock].configure(text=str(prix))

            if self.temps >= 1:  #au moins deux jours
                dernier = float(y.iloc[self.temps].item())
                avant_dernier = float(y.iloc[self.temps - 1].item())
                variation = dernier - avant_dernier
                pourcentage = (variation / avant_dernier) * 100
            else:
                variation = 0.0
                pourcentage = 0.0

            if variation >= 0:
                signe = "+"
                couleur = "green"
            else:
                signe="-"
                couleur="red"

            variation = abs(round(variation, 2))
            pourcentage = abs(round(pourcentage, 2))

            texte_rendement = f"{signe}{variation} $ ({signe}{pourcentage}%) la dernière journée."

            if stock not in self.rendement_labels:
                self.rendement_labels[stock] = ctk.CTkLabel(self,text=texte_rendement, text_color=couleur, font=("Arial", 14))
                self.rendement_labels[stock].grid(row=i, column=3, pady=(10,10))
            else:
                self.rendement_labels[stock].configure(text=f"{signe}{variation} $ ({signe}{pourcentage}%) la dernière journée.",text_color=couleur,  font=("Arial", 14))

        date_text = self.stocks[next(iter(self.stocks))].index[self.temps].date()

        if self.date_label is None:
            self.date_label = ctk.CTkLabel(self,text=date_text,text_color="light gray",font=("Arial", 24))
            self.date_label.grid(row=0, column=3, padx=(0,10), pady=(10,10))
        else:
            self.date_label.configure(text=date_text)

        self.temps += 1
        self.boucle_id = self.after(5000, self.boucle_stock)

    def clear_main_frame(self):
        if hasattr(self, "boucle_id"):
            try:
                self.after_cancel(self.boucle_id)
            except Exception:
                pass

        for widget in self.winfo_children():
            widget.destroy()
        
        
    def onButtonClicked(self, pseudo):
        self.clear_main_frame()
        Info(self.master, self.stocks, pseudo, self.temps, self.compte)

    def ouvrir_graph(self, name):
        self.clear_main_frame()
        Graph(self.master, self.stocks, name, self.temps, self.compte)

    def option_changed(self, value):
        """Ajoute un nouveau titre à la Watchlist du compte sélectionné."""
        #Ne rien faire si aucune sélection ou doublon
        if value == "Ajouter..." or value in self.stocks:
            return

        #Télécharger les données du nouveau titre
        try:
            df = yf.download(value, start="2024-01-01", end=self.date, interval="1d")
        except Exception as e:
            print(f"[ERREUR] Téléchargement des données pour {value} : {e}")
            return

        if df.empty:
            print(f"[ATTENTION] Aucune donnée trouvée pour {value}")
            return

        #Convertir les prix en float
        df["Close"] = df["Close"].astype(float)

        #Ajouter le titre à la watchlist locale
        self.stocks[value] = df

        # Si le compte existe, sauvegarder la nouvelle watchlist
        if self.compte is not None:
            self.compte.stocks = self.stocks
            self.compte.sauvegarder()
            print(f"{value} ajouté dans la Watchlist du compte {getattr(self.compte, 'nom', 'Inconnu')}")
        else:
            print("Aucun compte associé à cette Watchlist (ajout non sauvegardé).")

        

        #Stopper la boucle de mise à jour si elle tourne encore
        if hasattr(self, "boucle_id"):
            try:
                self.after_cancel(self.boucle_id)
            except Exception:
                pass

        # Supprimer les anciens widgets
        self.clear_main_frame()

        #réinitilaisation
        self.prix_buttons = {}
        self.rendement_labels = {}
        self.date_label = None

        #Recréer les widgets (avec le nouveau titre)
        self.create_widgets()

        # Relancer la boucle de mise à jour pour afficher immédiatement les prix
        self.boucle_stock()

        print(f"Affichage mis à jour : {value} visible dans la Watchlist.")




    def ouvrir_compte(self):
        actions = self.compte.action if self.compte is not None else {}
        argent = self.compte.argent if self.compte is not None else 1000

        self.clear_main_frame()

        from compte import Compte
        self.compte = Compte(self.master, self.stocks, self.temps, action=actions, argent = argent)

        self.compte.create_widgets()

    def acheter_stock(self, action):
        prix_achat = round(self.stocks[action]["Close"].iloc[self.temps - 1].iloc[0], 2)

        if self.compte is None:
            from compte import Compte
            self.compte = Compte(self.master, self.stocks, self.temps, action={}, argent=1000)

        if self.compte.argent >= prix_achat:
            self.compte.argent -= prix_achat

            if action in self.compte.action:
                ancienne_quantite = self.compte.action[action]["quantite"]
                ancien_prix = self.compte.action[action]["prix_achat"]

                nouveau_prix_moyen = ((ancien_prix * ancienne_quantite) + prix_achat) / (ancienne_quantite + 1)
                self.compte.action[action]["quantite"] += 1

            else:
                self.compte.action[action] = {"data": self.stocks[action], "prix_achat": prix_achat, "quantite": 1}

            self.compte.sauvegarder()
        else:
            self.label = ctk.CTkLabel(self, text="Pas assez de fonds pour acheter cette action",
                                    fg_color="dark gray", font=("Arial", 20))
            self.label.grid(row=3, column=3, padx=(20, 20), pady=(20, 20))
            self.after(3000, self.label.destroy)
    

    def supprime_stock(self, nom):
        #Stopper la boucle de mise à jour
        if hasattr(self, "boucle_id"):
            try:
                self.after_cancel(self.boucle_id)
            except Exception:
                pass

        #Supprimer le stock du dictionnaire
        if nom in self.stocks:
            del self.stocks[nom]

        #Sauvegarder la nouvelle liste
        if self.compte:
            self.compte.stocks = self.stocks
            self.compte.sauvegarder()

        self.prix_buttons = {}
        self.rendement_labels = {}
        self.date_label = None

        self.clear_main_frame()
        self.create_widgets()
        self.boucle_stock()

    
    def show_accueil(self):
        from accueil import Accueil
        self.clear_main_frame()
        self.destroy()
        self.current_page = Accueil(master=self.master) #Parent
        self.current_page.grid(row=0, column=0, sticky="nsew")

    def aller_A_accueil(self):
        self.show_accueil()