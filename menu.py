import customtkinter as ctk
import tkinter as tk
from tkinter import Menu
from info import Info
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

        info_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Informations", menu=info_menu)

        for stock in self.stocks:
            info_menu.add_command(label=stock, command=lambda s=stock : self.open_info(s))

        edit_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Édition", menu=edit_menu)
        edit_menu.add_command(label="Annuler", command=self.undo_action)
        edit_menu.add_command(label="Rétablir", command=self.redo_action)
        view_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Affichage", menu=view_menu)
        view_menu.add_command(label="Accueil", command=self.show_accueil)

    def open_info(self, stock):
        self.master.clear_main_frame()
        self.master.update_menu(self.stocks, self.temps, self.compte)
        Info(self.master, self.stocks, stock, self.temps, self.compte)
    def save_file(self):
        print("Enregistrer le fichier")
    def undo_action(self):
        print("Annuler")
    def redo_action(self):
        print("Rétablir")
    def show_accueil(self):
        print("Acceuile")

    
