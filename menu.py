import customtkinter as ctk
import tkinter as tk
from tkinter import Menu
from info import Info
from watchlist import Watchlist
from graphe import Graph
import pandas as pd

class MenuBar(ctk.CTkFrame):
    def __init__(self, master=None, stocks=None, temps=None, compte=None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.temps = temps
        self.compte = compte

        self.show_menu()

    def show_menu(self):

        menu_bar = Menu(self.master)
        self.master.configure(menu=menu_bar)

        # ajout du bouton quitter pour quitter l'app
        quitter_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Opérations", menu=quitter_menu)
        quitter_menu.add_command(label="Watchlist", command=self.open_watchlist)
        quitter_menu.add_separator()
        quitter_menu.add_command(label="Quitter", command=self.quit)
        

        # ajout du menu info
        info_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Informations", menu=info_menu)

        for stock in self.stocks:
            info_menu.add_command(label=stock, command=lambda s=stock : self.open_info(s))

        # ajout du menu graph
        graph_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Graphe", menu=graph_menu)

        for stock in self.stocks:
            graph_menu.add_command(label=stock, command=lambda s=stock : self.open_graph(s))

        # ajouter du menu compte
        compte_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Compte", menu=compte_menu)
        compte_menu.add_command(label="Ouvrir", command=self.open_compte)
        compte_menu.add_separator()
        compte_menu.add_command(label="Déconexion", command=self.deconexion)

    def open_info(self, stock):
        self.master.clear_main_frame()
        self.master.update_menu(self.stocks, self.temps, self.compte)
        Info(self.master, self.stocks, stock, self.temps, self.compte)
    
    def open_graph(self, stock):
        self.master.clear_main_frame()
        self.master.update_menu(self.stocks, self.temps, self.compte)
        Graph(self.master, self.stocks, stock, self.temps, self.compte)
    
    def open_watchlist(self):
        self.master.clear_main_frame()
        self.master.update_menu(self.stocks, self.temps, self.compte)
        Watchlist(self.master, self.stocks, self.temps, self.compte)

    def open_compte(self):
        actions = self.compte.action if self.compte is not None else {}
        argent = self.compte.argent if self.compte is not None else 1000

        self.master.clear_main_frame()

        from compte import Compte
        self.compte = Compte(self.master, self.stocks, self.temps, action=actions, argent = argent)

        self.master.update_menu(self.stocks, self.temps, self.compte)
        self.compte.create_widgets()

    def deconexion(self):
        self.master.clear_main_frame()
        self.master.update_menu(self.stocks, self.temps, self.compte)
        self.master.show_login()