import customtkinter as ctk

class Acheter(ctk.CTkFrame) :
    def __init__(self, master = None, stocks = None, temps = None, action = None, argent = None, user=None):
        super().__init__(master)
        self.master = master
        self.stocks = stocks
        self.action = action if action is not None else {}
        self.temps = temps
        self.argent = float(argent)
        self.user = user
        self.create_widgets()  
        

    def create_widgets(self):
        
         # Configuration principale
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

       
        self.titre_label = ctk.CTkLabel(self, text=f"Acheter : {self.action}", font=("Arial", 28, "bold"))
        self.titre_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        self.retour_button = ctk.CTkButton(self, text="⬅ Retour", fg_color="transparent", hover_color="cyan", font=("Arial", 28, "bold"), command=self.retour)
        self.retour_button.grid(row=0, column=2, padx=(20, 10), sticky="e")

    def clear_main_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

 
    def retour(self):
        from watchlist import Watchlist
        self.clear_main_frame()
        Watchlist(master=self.master, stocks=self.stocks,temps=self.temps,compte=None,user=self.user) 

       


        
        
        
        
    