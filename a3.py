"""
CSSE1001 Assignment 3
Semester 1, 2017
"""

import tkinter as tk
from random import randint
from tkinter import messagebox

import game_regular
import view
from base import BaseLoloApp
from highscores import HighScoreManager
from game_lucky7 import Lucky7Game
from game_make13 import Make13Game
from game_unlimited import UnlimitedGame
import game_objective

__author__ = "<Your name here>"
__email__ = "<Your student email here>"

__version__ = "1.0.2"


class LoloApp(BaseLoloApp):

    GAME_NAME = None

    def __init__(self, master, game, player_name):
        self._game = game
        self._master = master
        self._player_name = player_name

        self.set_game(self._game.GAME_NAME)

        self.LoloLogo = LoloLogo(self._master)
        self.LoloLogo.pack(side=tk.TOP)

        self._StatusBar = StatusBar(self._master)
        self._StatusBar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        if self.get_game() == "Objective":
            self._StatusBar.objective_mode(self._game.get_moves_remaining())
            self._StatusBar.update_objectives(self._game.get_objectives())

        menubar = tk.Menu(self._master)
        self._master.config(menu=menubar)

        dropdown = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=dropdown)
        dropdown.add_command(label="New Game", command=self.reset)
        dropdown.add_command(label="Save Score",
                             command=self.record_score)
        dropdown.add_command(label="Menu", command=self.return_to_menu)
        dropdown.add_command(label="Exit", command=self._master.destroy)

        self._master.title('Lolo :: %s Mode' % self._game.GAME_NAME)

        super().__init__(self._master, self._game)

        self._lightning_available = 1
        self._lightning_button = tk.Button(self._master,
                                           text="Lightning %i" %
                                           self._lightning_available,
                                           command=self.toggle_lightning)
        self._lightning_button.pack(side=tk.BOTTOM, pady=5)
        self._lightning = False
        self._lightning_is_disabled = False

        self.bind_keys()

    def return_to_menu(self):
        self._master.destroy()
        main()

    @classmethod
    def get_game(cls):
        return cls.GAME_NAME

    @classmethod
    def set_game(cls, game_mode):
        cls.GAME_NAME = game_mode

    def toggle_lightning(self):
        if not self._lightning:
            self.lightning_on()
        else:
            self.lightning_off()

        self._lightning = not self._lightning

    def lightning_on(self):
        self._grid_view.off('select', self.activate)
        self._grid_view.on('select', self.remove)
        self.update_active_lightning()

    def lightning_off(self):
        self._grid_view.on('select', self.activate)
        self._grid_view.off('select', self.remove)
        self.update_lightning()

    def lightning_disabled(self):
        self._lightning_button.config(state="disabled")
        self.update_active_lightning()
        self._master.unbind('<Control-l>')
        self._lightning_is_disabled = True

    def lightning_enabled(self):
        self._lightning_button.config(state="normal")
        self.update_lightning()
        self._lightning_is_disabled = False

    def update_lightning(self):
        self._lightning_button.config(text="Lightning %i" %
                                      self._lightning_available)

    def update_active_lightning(self):
        self._lightning_button.config(text="Lightning ACTIVE %i" %
                                      self._lightning_available)

    def remove(self, *positions):
        super().remove(*positions)
        if self._lightning:
            self._lightning_available -= 1
            self.update_lightning()
            self.toggle_lightning()
        if self._lightning_available == 0:
            self.lightning_disabled()
            if self._lightning:
                self.toggle_lightning()
            self.update_lightning()

    def activate(self, position):
        if self.get_game() == "Objective":
            self._game.set_objectives(self._game.check_objectives())
            self._StatusBar.compare_objective(self._game.get_objectives())
            self._StatusBar.check_game_win()
            print(self._game.get_objectives())
            print(self._game.get_static_objectives())

        if not self._game.can_activate(position) and not self._lightning:
            messagebox.showwarning("Invalid Activation",
                                   "You cannot activate this tile")
        else:
            lightning_chance = randint(1, 20)
            if lightning_chance == 10:
                self._lightning_available += 1
                self.lightning_enabled()
                if self._lightning_available > 0:
                    self._master.bind('<Control-l>', self.lightning_key)

        super().activate(position)

    def score(self, points):
        if self.get_game() == "Objective":
            self._StatusBar.objective_mode(self._game.get_moves_remaining())
        else:
            self._StatusBar.update_score(points)

    def bind_keys(self):
        self._master.bind('<Control-n>', self.reset_key)
        self._master.bind('<Control-l>', self.lightning_key)

    def lightning_key(self, event):
        self.toggle_lightning()

    def reset_key(self, event):
        self.reset()

    def reset(self):
        if self.get_game() == "Objective":
            self._game.set_moves_remaining(game_objective.ObjectiveGame.MOVES_REMAINING)
            self._StatusBar.reset_objective()
            self._StatusBar.update_objectives(self._game.get_static_objectives())
            self._game.set_objectives(self._game.get_static_objectives())
        self._game.reset()
        self._grid_view.draw(self._game.grid)
        self._lightning_available = 1
        self.update_lightning()
        self.bind_keys()

        if self._lightning_is_disabled:
            self.lightning_enabled()

        if self._lightning:
            self.toggle_lightning()

    def game_over(self):
        if self._lightning_available == 0 or \
           self._game.get_moves_remaining() == 0:
            messagebox.showwarning("Game over",
                                   "Game over, better luck next time!")
            self.record_score()
            if self.get_game() == "Objective":
                self.reset()
        else:
            messagebox.showwarning("Game over",
                                   "Game over," +
                                   "but you still have lightnings left.")

    def record_score(self):
        HighScoreManager().record(self._game.get_score(),
                                  self._game.grid,
                                  self._player_name)


class StatusBar(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self._master = master

        self._game_label = tk.Label(self, text=LoloApp.get_game())
        self._game_label.pack(side=tk.LEFT)

        self._score = tk.Label(self, text="Score: 0")
        self._score.pack(side=tk.RIGHT)

        if LoloApp.get_game() == "Objective":
            self._objective_frame = tk.Frame(self)
            self._objective_frame.pack()

            self._objectives_rem = tk.Label(self._objective_frame,
                                            text="Objectives Remaining :")
            self._objectives_rem.pack(anchor="center")

            self._construct_list = []
            self._objectives = []
            self._active_obj = {}
            self._won = False

    def update_score(self, points):
        self._score.config(text="Score: %i" % points)

    def update_objectives(self, objectives):
        colours = {
            1: "Red",
            2: "Blue",
            3: "Yellow",
            4: "Blue purple",
            5: "Pink",
            6: "Orange",
            7: "Dark Grey",
            8: "Green",
            9: "Brown",
            10: "Dark Blue",
            11: "Pale Blue",
            12: "Beige",
            13: "Lime"
        }
        retrieved_objectives = False
        if not retrieved_objectives:
            self._objectives = objectives
            retrieved_objectives = True

        for type, value in self._objectives:
            if (colours[type], value) not in self._construct_list:
                self._construct_list.append((colours[type], value))

        x = 1
        while len(self._construct_list) > 0:
            self._construct_list[0] = tk.Label(self._objective_frame,
                                               text=self._construct_list[0])
            self._construct_list[0].pack()
            self._active_obj[x] = self._construct_list[0]
            x += 1
            del self._construct_list[0]

    def compare_objective(self, retrieved):
        for objective in self._objectives:
            if objective not in retrieved:
                self._active_obj[objective[0]].destroy()

    def check_game_win(self):
        if len(game_objective.ObjectiveGame.get_objectives()) < 1 and \
           not self._won:
            tk.messagebox.showwarning("Win!",
                                      "You have successfully eliminated" +
                                      " all objectives")
            self._won = True

    def objective_mode(self, moves):
        self._score.config(text="Moves Remaining: %i" % moves)

    def reset_objective(self):
        for label in self._active_obj:
            self._active_obj[label].destroy()


class LoloLogo(tk.Canvas):

    def __init__(self, master):
        super().__init__(master)

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


class AutoPlayingGame(BaseLoloApp):

    def __init__(self, master):
        super().__init__(master)
        self._game = GameMode.get_game()
        self._game_mode_selection = GameMode.GAME_MODE
        self.play()
        self.check_changes()
        self._grid_view.off('select', self.activate)

    def play(self):
        row_size, col_size = self._game.grid.size()
        try:
            position = (randint(0, row_size), randint(0, col_size))
            if position in self._game.grid:
                if self._game.can_activate(position):
                    self.activate(position)
                else:
                    while not self._game.is_resolving():
                        self.play()
            self._master.after(2000, self.play)
        except RecursionError:
            self.reset()

    def check_changes(self):
        new_mode = GameMode.GAME_MODE
        if new_mode != self._game_mode_selection:
            self._game = GameMode.get_game()
            self._game_mode_selection = GameMode.GAME_MODE
            self.repack()
        self._master.after(2000, self.check_changes)

    def game_over(self):
        self.reset()

    def reset(self):
        self._game.reset()
        self._grid_view.draw(self._game.grid)

    def repack(self):
        self._grid_view.pack_forget()
        self._grid_view = view.GridView(self._master, self._game.grid.size())
        self._grid_view.pack()
        self._grid_view.draw(self._game.grid)

    def score(self, points):
        pass


class Replay:

    def __init__(self, master, game):
        grid_view = view.GridView(master, game.grid.size())
        grid_view.pack()
        grid_view.draw(game.grid)


class HighScore(HighScoreManager):

    def __init__(self, master):
        super().__init__(gamemode=GameMode.GAME_MODE)

        self._master = master
        self._master.title("Leaderboards :: Lolo")

        self._best_player = self.get_sorted_data()
        self._best_player_label = tk.Label(self._master,
                                           text="Best Player: " +
                                           self._best_player[0]['name'] +
                                           " with " +
                                           str(self._best_player[0]['score']) +
                                           " points!")
        self._best_player_label.pack()

        game = game_regular.RegularGame.deserialize(self._best_player[0]['grid'])
        replay = Replay(self._master, game)

        self._lb_label = tk.Label(self._master, text="Leaderboard")
        self._lb_label.pack()

        self.load()
        self._row = 0
        self._frames = 0
        self._new_frame = []
        while self._frames < len(self.get_data()):
            self._new_frame.append("frame" + str(self._frames))
            self._frames += 1
            if self._frames > 15:
                break

        for data in self.get_sorted_data():
            self.add_row(data['name'], data['score'])

    def add_row(self, name, score):
        self._new_frame[self._row] = tk.Frame(self._master)
        self._new_frame[self._row].pack(fill=tk.X, padx=20)

        name = tk.Label(self._new_frame[self._row], text=name)
        name.pack(side=tk.LEFT)

        score = tk.Label(self._new_frame[self._row], text=score)
        score.pack(side=tk.RIGHT)

        self._row += 1


class GameMode:

    GAME_MODE = "regular"

    def __init__(self, master):
        self._master = master
        self._game = tk.StringVar()
        game_modes = ["regular",
                      "make13",
                      "lucky7",
                      "unlimited",
                      "objective"]

        for game_mode in game_modes:
            mode_button = tk.Radiobutton(self._master,
                                         text=game_mode.title()+" mode",
                                         variable=self._game,
                                         value=game_mode)
            mode_button.pack()
            if game_mode == GameMode.GAME_MODE:
                mode_button.invoke()

        self._button = tk.Button(self._master,
                                 text="Confirm",
                                 command=self.set_game)
        self._button.pack()

    def set_game(self):
        self._master.destroy()
        self.set_class_var(self._game.get())

    @classmethod
    def set_class_var(cls, game_mode):
        cls.GAME_MODE = game_mode

    @classmethod
    def get_game(cls):
        if cls.GAME_MODE == "regular":
            return game_regular.RegularGame()
        elif cls.GAME_MODE == "make13":
            return Make13Game()
        elif cls.GAME_MODE == "lucky7":
            return Lucky7Game()
        elif cls.GAME_MODE == "unlimited":
            return UnlimitedGame()
        elif cls.GAME_MODE == "objective":
            return game_objective.ObjectiveGame()


class LoadingScreen:

    def __init__(self, master):

        self._master = master

        self._master.geometry("1000x800")
        self._master.title("Lolo")

        self.LoloLogo = LoloLogo(self._master)
        self.LoloLogo.pack(anchor="center", expand=True)

        self._entry_frame = tk.Frame(self._master)
        self._entry_frame.pack()

        self._player_name = tk.Entry(self._entry_frame)
        self._player_name.pack(side=tk.RIGHT)

        self._your_name = tk.Label(self._entry_frame, text="Your Name :")
        self._your_name.pack(side=tk.LEFT)

        self._left_frame = tk.Frame(self._master)
        self._left_frame.pack(side=tk.LEFT, anchor="w", expand=True, padx=20,
                              pady=20, fill=tk.X)

        self._right_frame = tk.Frame(self._master)
        self._right_frame.pack(side=tk.RIGHT, anchor="e", expand=False, padx=20,
                               pady=20)

        self._play_game = tk.Button(self._left_frame, text="New Game",
                                    command=self.new_game)
        self._play_game.pack(side=tk.TOP, ipadx=63, pady=30)

        self._game_mode = tk.Button(self._left_frame, text="Game mode",
                                    command=self.game_mode)
        self._game_mode.pack(side=tk.TOP, ipadx=63, pady=30)

        self._highscore = tk.Button(self._left_frame, text="High Scores",
                                    command=self.highscore)
        self._highscore.pack(side=tk.TOP, ipadx=60, pady=30)

        self._exit = tk.Button(self._left_frame, text="Exit Game",
                               command=self._master.destroy)
        self._exit.pack(side=tk.TOP, ipadx=66, pady=30)

        loading_lolo = AutoPlayingGame(self._right_frame)

    def new_game(self):
        player_name = self._player_name.get()

        if player_name == '':
            messagebox.showwarning("Please enter a name.",
                                   "Please enter a name.")
        else:
            self._master.withdraw()
            game = GameMode.get_game()
            window = tk.Toplevel()
            LoloGame = LoloApp(window, game, player_name)

    @staticmethod
    def highscore():
        window = tk.Toplevel()
        highscores = HighScore(window)

    @staticmethod
    def game_mode():
        window = tk.Toplevel()
        game_mode = GameMode(window)


def main():
    root = tk.Tk()
    window = LoadingScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()