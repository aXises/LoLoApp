"""
CSSE1001 Assignment 3
Semester 1, 2017
"""

import tkinter as tk
from random import randint
from base import BaseLoloApp
from tkinter import messagebox

import game_regular
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
        self._master = master

        GAME_NAME = self._game.GAME_NAME

        self.set_game(GAME_NAME)

        self.LoloLogo = LoloLogo(master)
        self.LoloLogo.pack(side=tk.TOP)

        self._StatusBar = StatusBar(master)
        self._StatusBar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        menubar = tk.Menu(master)
        self._master.config(menu=menubar)

        dropdown = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=dropdown)
        dropdown.add_command(label="New Game", command=self.reset)
        dropdown.add_command(label="Exit", command=master.destroy)

        self._master.title('Lolo :: %s Mode' % GAME_NAME)

        super().__init__(master, game)
        self._master = master

        self._lightning_available = 1
        self._lightning_button = tk.Button(master,
                                           text="Lightning %i" %
                                           self._lightning_available,
                                           command=self.toggle_lightning)
        self._lightning_button.pack(side=tk.BOTTOM, pady=5)
        self._lightning = False

        self.bind_keys()

    @classmethod
    def get_game(cls):
        return cls.GAME_NAME

    @classmethod
    def set_game(cls, game_mode):
        cls.GAME_NAME = game_mode

    def toggle_lightning(self):
        if not self._lightning:
            self._grid_view.off('select', self.activate)
            self._grid_view.on('select', self.remove)
            self._lightning_button.config(text="Lightning ACTIVE %i" %
                                          self._lightning_available)
        else:
            self._grid_view.on('select', self.activate)
            self._grid_view.off('select', self.remove)
            self._lightning_button.config(text="Lightning %i" %
                                          self._lightning_available)

        self._lightning = not self._lightning

    def remove(self, *positions):
        super().remove(*positions)
        if self._lightning:
            self._lightning_available -= 1
            self._lightning_button.config(text="Lightning ACTIVE %i" %
                                               self._lightning_available)
            if self._lightning_available == 0:
                self._lightning_button.config(state="disabled",
                                              text="Lightning %i" %
                                              self._lightning_available)
                self._master.unbind('<Control-l>')
                self.toggle_lightning()

    def activate(self, position):
        try:
            super().activate(position)
        except IndexError:
            messagebox.showwarning("Invalid Activation",
                                   "You cannot activate this tile")

        lightning_chance = randint(randint(1, 5), randint(15, 20))
        if lightning_chance == 10:
            self._lightning_available += 1
            self._lightning_button.config(state="normal",
                                          text="Lightning %i" %
                                          self._lightning_available)
            if self._lightning_available > 0:
                self._master.bind('<Control-l>', self.lightning_key)

    def score(self, points):
        self._StatusBar.update_score(points)

    def bind_keys(self):
        self._master.bind('<Control-n>', self.reset_key)
        self._master.bind('<Control-l>', self.lightning_key)

    def lightning_key(self, event):
        self.toggle_lightning()

    def reset_key(self, event):
        self.reset()

    def reset(self):
        self._game.reset()
        self._grid_view.draw(self._game.grid)
        self._game.set_score(0)

    def game_over(self):
        if self._lightning_available == 0:
            messagebox.showwarning("Game over",
                                   "Better luck next time!")
        else:
            messagebox.showwarning("Game over",
                                   "Game over," +
                                   "but you still have lightnings left.")


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
        super().__init__(canvas)

        self.config(width=400, height=100)

        # L
        self.create_rectangle(15, 100, 35, 20, fill="purple", width=0)
        self.create_rectangle(15, 80, 95, 100, fill="purple", width=0)

        # O
        self.create_oval(115, 20, 195, 100, fill="purple", width=0)
        self.create_oval(145, 55, 175, 85, fill="white", width=0)

        # L
        self.create_rectangle(215, 100, 235, 20, fill="purple", width=0)
        self.create_rectangle(215, 80, 295, 100, fill="purple", width=0)

        # O
        self.create_oval(315, 20, 395, 100, fill="purple", width=0)
        self.create_oval(345, 55, 375, 85, fill="white", width=0)


class LoadingScreen:

    def __init__(self, master):

        self._master = master

        self._master.geometry("1000x600")
        self._master.title("Lolo")

        self.LoloLogo = LoloLogo(master)
        self.LoloLogo.pack(anchor="center", expand=True)

        self._left_frame = tk.Frame(master)
        self._left_frame.pack(side=tk.LEFT, anchor="w", expand=True, padx=20,
                              pady=20, fill=tk.X)

        self._right_frame = tk.Frame(master)
        self._right_frame.pack(side=tk.RIGHT, anchor="e", expand=False, padx=20,
                               pady=20)

        self._play_game = tk.Button(self._left_frame, text="New Game",
                                    command=self.new_game)
        self._play_game.pack(side=tk.TOP, ipadx=63, pady=30)

        self._highscore = tk.Button(self._left_frame, text="High Scores")
        self._highscore.pack(side=tk.TOP, ipadx=60, pady=30)

        self._exit = tk.Button(self._left_frame, text="Exit Game",
                               command=self._master.destroy)
        self._exit.pack(side=tk.TOP, ipadx=66, pady=30)

        loading_lolo = AutoPlay(self._right_frame)

    @staticmethod
    def new_game():
        game = game_regular.RegularGame()
        # game = game_make13.Make13Game()
        # game = game_lucky7.Lucky7Game()
        # game = game_unlimited.UnlimitedGame()
        window = tk.Toplevel()
        LoloGame = LoloApp(window, game)


def main():

    root = tk.Tk()
    window = LoadingScreen(root)
    root.mainloop()


if __name__ == "__main__":
    main()
