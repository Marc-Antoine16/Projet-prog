import os
import json

class User :
    def __init__(self, username, password, balance, stocks_owned):
        
        self.username = username
        self.password = password
        self.balance = balance
        self.stocks_owned = stocks_owned if stocks_owned is not None else [] # si il existe une liste la prendre sinon la crée
    
    def add_stock(self, stock) :
        if not stock in self.stocks_owned :
            self.stocks_owned.append(stock)

        self.save_to_json()

    def remove_stock(self, stock) :

        if stock in self.stocks_owned : 
            self.stocks_owned.remove(stock)
            self.save_to_json()
    
    def change_balence(self, amount) :
        self.balance = amount

    def save_to_json(self, users_file="users.json"):
       
        if not os.path.exists(users_file):
            return

        with open(users_file, "r") as f:
            users = json.load(f)

        for user in users:
            if user["username"] == self.username:
                user["balance"] = self.balance
                user["stocks_owned"] = self.stocks_owned
                break

        with open(users_file, "w") as f:
            json.dump(users, f, indent=4)