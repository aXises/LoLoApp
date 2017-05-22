"""
CSSE1001 Assignment 3
Semester 1, 2017
"""

import tkinter as tk
from base import BaseLoloApp

# # For alternative game modes
# from game_make13 import Make13Game
# from game_lucky7 import Lucky7Game
# from game_unlimited import UnlimitedGame

__author__ = "<Your name here>"
__email__ = "<Your student email here>"

__version__ = "1.0.2"


# Once you have created your basic gui (LoloApp), you can delete this class
# and replace it with the following:
# from base import BaseLoloApp

# Define your classes here


class LoloApp(BaseLoloApp):

    def __init__(self, master, game):

        self._LoloLogo = LoloLogo(master)
        self._LoloLogo.pack(side=tk.TOP, anchor="n", expand=True, fill=tk.BOTH)

        self._StatusBar = StatusBar(master)
        self._StatusBar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        super().__init__(master)

        self._master = master
        self._game = game

        master.title('Lolo :: %s Mode' % self._game.GAME_NAME)

        menubar = tk.Menu(master)
        master.config(menu=menubar)

        dropdown = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=dropdown)
        dropdown.add_command(label="New Game", command=self.reset)
        dropdown.add_command(label="Exit", command=master.destroy)

    def reset(self):
        pass

class StatusBar(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        Game = tk.Label(self, text="game")
        Game.pack(side=tk.LEFT)

        Score = tk.Label(self, text="score")
        Score.pack(side=tk.RIGHT)

    def set_game(self, game_mode):
        pass

    def set_score(self, score):
        pass


class LoloLogo(tk.Canvas):

    def __init__(self, canvas):
        super().__init__()

        self.config(width=200, height=100)
        self.create_rectangle(20, 100, 30, 20, fill="purple")


def main():
    pass
    # Your GUI instantiation code here


if __name__ == "__main__":
    main()
