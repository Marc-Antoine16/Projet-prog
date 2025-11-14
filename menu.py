import customtkinter as ctk
import tkinter as tk
from tkinter import Menu
from info import Info
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
        quitter_menu.add_command(label="Quitter", command=self.quit)
        menu_bar.add_cascade(label="Quitter", menu=quitter_menu)

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

        # view_menu = Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label="Affichage", menu=view_menu)
        # view_menu.add_command(label="Accueil", command=self.show_accueil)

    def open_info(self, stock):
        self.master.clear_main_frame()
        self.master.update_menu(self.stocks, self.temps, self.compte)
        Info(self.master, self.stocks, stock, self.temps, self.compte)
    
    def open_graph(self, stock):
        self.master.clear_main_frame()
        self.master.update_menu(self.stocks, self.temps, self.compte)
        Graph(self.master, self.stocks, stock, self.temps, self.compte)
 

    
