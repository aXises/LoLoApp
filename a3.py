"""
CSSE1001 Assignment 3
Semester 1, 2017
"""

import tkinter as tk
from random import randint
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

    GAME_NAME = None

    def __init__(self, master, game):
        self._game = game

        GAME_NAME = self._game.GAME_NAME

        self.set_game(GAME_NAME)

        self._LoloLogo = LoloLogo(master)
        self._LoloLogo.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self._StatusBar = StatusBar(master)
        self._StatusBar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        menubar = tk.Menu(master)
        master.config(menu=menubar)

        dropdown = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=dropdown)
        dropdown.add_command(label="New Game", command=self.reset)
        dropdown.add_command(label="Exit", command=master.destroy)

        master.title('Lolo :: %s Mode' % GAME_NAME)

        super().__init__(master, game)
        self._master = master

        self.lightning_available = 1
        self._lightning_button = tk.Button(master,
                                           text="Lightning %i" %
                                           self.lightning_available,
                                           command=self.lightning)
        self._lightning_button.pack(side=tk.BOTTOM, pady=5)
        self.lightning = False

    def lightning(self):

        if not self.lightning:
            print('lightning on')
            self._grid_view.on('select', self.activate)
        else:
            print('lightning off')
            self._grid_view.off('select', self.activate)

        self.lightning = not self.lightning

    def activate(self, position):
        self.remove(position)
        #print('test')

    def score(self, points):
        self._StatusBar.update_score(points)

    @classmethod
    def get_game(cls):
        return cls.GAME_NAME

    @classmethod
    def set_game(cls, game_mode):
        cls.GAME_NAME = game_mode

    def reset(self):
        #Todo
        #self._grid_view.destroy()
        #self._grid_view.draw(self._game.grid, self._game.find_connections())
        pass


class StatusBar(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self._game = tk.Label(self, text=LoloApp.get_game())
        self._game.pack(side=tk.LEFT)

        self._score = tk.Label(self, text="Score: 0")
        self._score.pack(side=tk.RIGHT)

    def update_score(self, points):
        self._score.config(text="Score: %i" % points)


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
