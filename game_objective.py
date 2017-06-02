import game_regular
import json

__author__ = "<Your name here>"
__email__ = "<Your student email here>"
__version__ = "1.1.2"

class ObjectiveGame(game_regular.RegularGame):
    """Objective game mode.
    
    Specific tiles types must be combined to achieve a objective.
    
    The game is won when all objectives are completed.
    """

    GAME_NAME = "Objective"
    OBJECTIVES = []
    MOVES_REMAINING = 20
    GRID = []

    def __init__(self, size=(6,6), types=3, min_group=2):
        """Constructor

        Parameters which to default to if JSON data for objective game mode
        cannot be loaded.
        
        Parameters:
            size (tuple<int, int>): The number of (rows, columns) in the game.
            initial_tiles (int): The number of tiles.
            min_group (int): The minimum number of tiles required for a
                             connected group to be joinable.
        """

        data = self.load()
        self.set_moves_remaining(data["limit"])
        self._moves_remaining = ObjectiveGame.MOVES_REMAINING
        self._objectives = []

        for list in data["objectives"]:
            objective = tuple(list)
            self._objectives.append(objective)

        self.set_objectives(self._objectives)

        if data["grid"] != "None":
            self.set_grid(data["grid"])

        super().__init__(data["size"], data["types"], data["min_group"])

    @staticmethod
    def load():
        """Loads the objective_mode JSON file."""
        with open("objective_mode.json") as json_data:
            data = json.load(json_data)
            json_data.close()
        return data

    def check_objectives(self):
        """
        Checks the objectives currently active or/if has been completed.
        Returns:
            (list): The objectives remaining.
        """

        objective = []
        while not self.is_resolving():
            for group in self.grid.find_all_connected():
                for position in group:
                    cell = self.grid[position]
                    for type, value in self.get_objectives():
                        if type == cell.get_type() and value <= cell.get_value():
                            objective.append((type, value))
                            if len(objective) > 0:
                                return set(self.get_objectives()) - set(objective)
            break
        return self.get_objectives()

    def activate(self, position):
        """
        Attempts to activate the tile at the given position.
        
        Parameters:
            position (tuple<int, int>): Row-column position of the tile.
            
        Returns:
            (RegularGame.activate): The method to execute.
            
        """

        self._moves_remaining -= 1
        return game_regular.RegularGame.activate(self, position)

    @classmethod
    def set_grid(cls, grid):
        """Sets the game grid.
        
        Parameter:
            grid (list): The grid to be serialized in to the game.
        """

        cls.GRID = grid

    @classmethod
    def get_grid(cls):
        """
        Gets the game grid.
        
        Returns:
            (list): The grid to be serialized in to the game.
        """

        return cls.GRID

    @classmethod
    def set_objectives(cls, objectives):
        """Sets the game objectives.

        Parameter:
            objectives (list): The objectives for the game.
        """

        cls.OBJECTIVES = objectives

    @classmethod
    def get_objectives(cls):
        """Sets the game grid.

        Returns:
            (list): The objectives for the game.
        """
        return cls.OBJECTIVES

    def get_static_objectives(self):
        """
        Gets the initial objectives.
        
        Returns:
            (list): The initial objectives for the game.
        """

        return self._objectives


    def set_moves_remaining(self, moves):
        """
        Sets the moves remaining.

        Parameter:
            moves (int): The moves remaining for the player
        """
        
        self._moves_remaining = moves

    def get_moves_remaining(self):
        """
        Gets the moves remaining.
        
        Returns:
            (int): The moves remaining for the player
        """

        return self._moves_remaining


    def game_over(self):
        """Handles the game ending.
        
        Returns:
            True (Bool): Whether if the game is over or not.
        """

        if self.get_moves_remaining() == 0:
            return True
