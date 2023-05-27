#!/usr/bin/env python3

import random
from tkinter import *
from tkinter import messagebox
import requests
import requests.utils
import yaml

DRINK_MENU = "../../drinks.yaml"
DRINK_API = "https://www.thecocktaildb.com/api/json/v1/1/"
THEME_COLOR = "#375362"
TEXT = ("Arial", 15, "normal")


class GUI:
    def __init__(self):
        window = Tk()
        window.title("Wes' Bar")
        window.config(padx=50, pady=50, bg=THEME_COLOR)
        self.available_drinks = {}
        self.button_img = None
        self.radio_state = StringVar()
        self.interface()
        window.mainloop()

    def interface(self):
        with open(DRINK_MENU, encoding="UTF-8") as file:
            drinks = yaml.safe_load(file)["Drinks"]

        for index, drink in enumerate(drinks):
            self.available_drinks[drink] = Radiobutton(text=drink,
                                                       value=drink,
                                                       variable=self.radio_state,
                                                       bg=THEME_COLOR,
                                                       highlightthickness=0,
                                                       font=TEXT)
            self.available_drinks[drink].grid(column=1, row=index)
        surprise_me = Radiobutton(text="Surprise Me!",
                                  value="surprise",
                                  variable=self.radio_state,
                                  bg=THEME_COLOR,
                                  highlightthickness=0,
                                  font=TEXT)
        surprise_me.grid(column=1, row=len(drinks))

        self.button_img = PhotoImage(file="images/true.png")
        drink_button = Button(image=self.button_img,
                              height=100,
                              width=100,
                              bg=THEME_COLOR,
                              pady=25,
                              highlightthickness=0,
                              command=self.get_drink)
        drink_button.grid(column=1, row=len(drinks) + 1, columnspan=2)

    def get_drink(self):
        if self.radio_state.get() == "surprise":
            response = requests.get(url=f"{DRINK_API}random.php")
            data = response.json()
            name, ingredients, instructions = self.parse_drink(data)
            messagebox.showinfo(title=name, message=f"{ingredients}\nInstructions:\n{instructions}")
        else:
            params = {
                "i": self.radio_state.get()
            }
            response = requests.get(url=f"{DRINK_API}filter.php", params=params)
            data = response.json()
            drink_id = random.choice(data["drinks"])
            drink_id = drink_id["idDrink"]

            params = {
                "i": drink_id
            }
            response = requests.get(url=f"{DRINK_API}lookup.php", params=params)
            data = response.json()
            name, ingredients, instructions = self.parse_drink(data)
            messagebox.showinfo(title=name, message=f"{ingredients}\nInstructions:\n{instructions}")

    def parse_drink(self, data: dict) -> str:
        name = data["drinks"][0]["strDrink"]
        instructions = data["drinks"][0]["strInstructions"]

        ingredients = "Ingredients:\n"
        for count in range(1, 15):
            i = data["drinks"][0][f"strIngredient{count}"]
            m = data["drinks"][0][f"strMeasure{count}"]
            if i is not None:
                ingredients += f"{count}. {i} -- {m}\n"
        return name, ingredients, instructions
