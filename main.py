import customtkinter as ctk
from accueil import Accueil


APP_GEOMETRY = "900x600"
APP_TITLE = "Paper Trading"

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")      
        self.geometry(APP_GEOMETRY)
        self.title(APP_TITLE)

        self.temps_global=0
        self.jour_global =0

        self.freeze_date = False

        self.protocol("WM_DELETE_WINDOW", self.quit) #ferme l'appli
        self.show_accueil() 

    def show_accueil(self):
        self.current_page = Accueil(master=self)
        self.current_page.grid(row=0, column=0, sticky="nsew") #nsew: le widget s’aligne au centre de la cellule et s’étire avec la fenêtre.
    
if __name__ == "__main__":
    app = MainApp() 
    app.mainloop()