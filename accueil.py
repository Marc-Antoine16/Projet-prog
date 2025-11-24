import customtkinter as ctk
from titreDetenues import TitreDetenues
from creation import Creation
from graph_total import GraphTotal
import json
import os
import yfinance as yf
from datetime import date


class Accueil(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Cache pour les DataFrames de prix (évite de télécharger 1000 fois)
        self.df_cache = {}

        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.create_widgets()

    def create_widgets(self):

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Le frame a plusieurs lignes/colonnes extensibles
        self.grid_rowconfigure((0, 1, 2, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)

        self.titre_label = ctk.CTkLabel(self, text="Accueil", font=("Arial", 32, "bold"))
        self.titre_label.grid(row=0, column=3, pady=(10, 10))

        solde_total = self.calculer_solde_total()

        self.bouton_solde = ctk.CTkButton(self, text=f"Solde total : {solde_total:.2f} $",font=("Arial", 20),command=self.ouvrir_graph_total)
        self.bouton_solde.grid(row=1, column=3, pady=(10, 10))

        self.bouton_titres = ctk.CTkButton(self,text="Titres détenus →",font=("Arial", 20),command=self.ouvrir_titreDetenues)
        self.bouton_titres.grid(row=3, column=3, pady=(10, 10))

        self.compte_label = ctk.CTkLabel(self, text="Compte(s)", font=("Arial", 24))
        self.compte_label.grid(row=5, column=1, pady=(10, 10))

        self.bouton_creation = ctk.CTkButton(self, text="Créer un compte",fg_color="transparent",hover_color="red",font=("Arial", 20),command=self.creer_compte)
        self.bouton_creation.grid(row=6, column=1, pady=(10, 10))

        self.afficher_compte()

        # Lance la mise à jour périodique du solde total
        self.boucle_solde()

    def charger_comptes(self):
        """Charge la liste des comptes depuis comptes.json."""

        if not os.path.exists("comptes.json"):
            return []

        try:
            with open("comptes.json", "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []

    def get_df_symbole(self, symbole):
        """Retourne le DataFrame de prix pour un symbole (avec cache)."""
        if symbole in self.df_cache:
            return self.df_cache[symbole]

        try:
            df = yf.download(symbole, start="2024-01-01", end=date.today(), interval="1d", progress=False)
            if df.empty or "Close" not in df:
                print(f"Aucune donnée valide pour {symbole}")
                self.df_cache[symbole] = None
                return None

            df["Close"] = df["Close"].astype(float)
            self.df_cache[symbole] = df
            return df

        except Exception as e:
            print(f"ERREUR Téléchargement de {symbole} : {e}")
            self.df_cache[symbole] = None
            return None


    def afficher_compte(self):
        data = self.charger_comptes()

        if len(data) > 0:
            self.msgAide = ctk.CTkLabel(self,text="Compte créé ! Appuyez sur un de vos compte(s) pour commencer à négocier.",text_color="green",font=("Arial", 16))
            self.msgAide.grid(row=4, column=3, pady=(10, 10))

            comptes_afficher = data[-3:]

            for i, compte in enumerate(comptes_afficher):
                nom = compte.get("nom", "Inconnu")
                montant = compte.get("montant", 0)
                bouton_compte = ctk.CTkButton(self,text=f"{nom} — {montant:.2f} $",font=("Arial", 20),command=lambda c=compte: self.ouvrir_infoCompte(c))
                bouton_compte.grid(row=5 + i, column=3, pady=(10, 10))
            return

        self.label_aucun = ctk.CTkLabel(self,text="Aucun compte n'a encore été créé.",font=("Arial", 20),text_color="gray")
        self.label_aucun.grid(row=5, column=3, pady=(10, 10))

    def boucle_solde(self):
        """Met à jour le texte du solde total périodiquement."""

        if not self.winfo_exists():
            return

        # Si le bouton est détruit, on arrête aussi
        if not self.bouton_solde.winfo_exists():
            return

        nouveau_solde = self.calculer_solde_total()
        self.bouton_solde.configure(text=f"Solde total : {nouveau_solde:.2f} $")

        # Relance dans 5 s
        self.boucle_id = self.after(5000, self.boucle_solde)

    def calculer_solde_total(self):
        """Calcule le solde total de tous les comptes en comptant l'évolution des actions."""

        total = 0.0
        comptes = self.charger_comptes()

        t = int(getattr(self.master, "temps_global", 0))

        for compte in comptes:
            # Argent liquide
            total += float(compte.get("montant", 0.0))

            # Actions détenues
            actions = compte.get("actions", {})
            for symbole, info in actions.items():
                quantite = info.get("quantite", 0)
                prix_achat = float(info.get("prix_achat", 0))

                if quantite <= 0 or prix_achat <= 0:
                    continue

                df = self.get_df_symbole(symbole)
                if df is None:
                    # fallback : utilise le prix d'achat si pas de données
                    valeur = prix_achat * quantite
                else:
                    serie = df["Close"]
                    if len(serie) == 0:
                        valeur = prix_achat * quantite
                    else:
                        idx = t
                        if idx >= len(serie):
                            idx = len(serie) - 1
                        prix_actuel = float(serie.iloc[idx])
                        valeur = prix_actuel * quantite

                total += valeur

        return total

    def ouvrir_infoCompte(self, compte_data):
        """Ouvre la Watchlist du compte sélectionné avec ses données sauvegardées."""

        self.clear_main_frame()
        from watchlist import Watchlist
        from compte import Compte

        # Recharger les tickers de la Watchlist
        watchlist_data = {}
        from datetime import date as dt_date
        import yfinance as yf
        import pandas as pd

        for ticker in compte_data.get("watchlist", []):
            try:
                df = yf.download(ticker, start="2024-01-01", end=dt_date.today(), interval="1d", progress=False)
                if not df.empty:
                    df["Close"] = df["Close"].astype(float)
                    watchlist_data[ticker] = df
            except Exception as e:
                print(f"[ERREUR] lors du chargement du ticker {ticker} :", e)

        # Recharger les actions, en évitant les téléchargements inutiles
        actions_data = compte_data.get("actions", {})
        for symbole, infos in actions_data.items():
            try:
                if symbole in watchlist_data:
                    infos["data"] = watchlist_data[symbole]
                else:
                    df = yf.download(symbole, start="2024-01-01", end=dt_date.today(), interval="1d", progress=False)
                    if not df.empty:
                        df["Close"] = df["Close"].astype(float)
                        infos["data"] = df
            except Exception as e:
                print(f"[ERREUR] lors du chargement de l'action {symbole} :", e)

        # Crée le Compte
        compte = Compte(master=self.master,stocks=watchlist_data,temps=0,action=actions_data,argent=compte_data.get("montant", 0),nom=compte_data.get("nom", "Inconnu"))

        setattr(compte, "nom", compte_data.get("nom", "Inconnu"))

        # Ouvre la Watchlist liée à ce compte
        self.destroy()
        self.master.current_page = Watchlist(master=self.master, compte=compte, temps=1)
        self.master.current_page.grid(row=0, column=0, sticky="nsew")

        print(f"Compte '{compte.nom}' ouvert avec {len(watchlist_data)} titres et {len(actions_data)} actions.")

    def ouvrir_titreDetenues(self):
        self.clear_main_frame()
        TitreDetenues(self.master)

    def ouvrir_graph_total(self):
        comptes = self.charger_comptes()
        if not comptes:
            msgAide = ctk.CTkLabel(self,text="Veuillez créer au moins un compte pour voir le graphique du rendement total.",text_color="red",font=("Arial", 16))
            msgAide.grid(row=4, column=3, pady=(10, 10))
            return

        self.clear_main_frame()
        self.master.current_page = GraphTotal(master=self.master)
        self.master.current_page.grid(row=0, column=0, sticky="nsew")

    def creer_compte(self):
        data = self.charger_comptes()

        if len(data) > 2:
            # Trop de comptes
            tropDeCompte = ctk.CTkLabel(self, text="Vous avez atteint le maximum de trois comptes !",text_color="red",font=("Arial", 16))
            tropDeCompte.grid(row=4, column=3, pady=(10, 10))
        else:
            self.clear_main_frame()
            Creation(self.master)

    def clear_main_frame(self):
        # Arrête les after éventuels
        if hasattr(self, "boucle_id"):
            try:
                self.after_cancel(self.boucle_id)
            except Exception:
                pass

        for widget in self.winfo_children():
            widget.destroy()
