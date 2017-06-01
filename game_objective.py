"""Modelling classes for Objective game mode."""

import game_regular

__author__ = "<Your name here>"
__email__ = "<Your student email here>"
__version__ = "1.1.2"


class ObjectiveTile(game_regular.RegularTile):
    """Tile whose value & type are equal, incrementing by one when joined."""

    def __init__(self, type, value=1):
        """Constructor

        Parameters:
             value (int): The tile's value.
        """
        super().__init__(type, value)
        self._value = value
        self._type = type

class ObjectiveGame(game_regular.RegularGame):

    GAME_NAME = "Objective"
    OBJECTIVES = []

    def __init__(self, size=(6,6), types=3, min_group=2, objective_value="obj",
                 objective_type=13, normal_weight=20, max_weight=2):

        # Basic properties
        self._objective_type = objective_type
        self._objective_value = objective_value
        self._moves_remaining = 50
        self._objectives = [(1, 10), (2, 20), (3, 15)]
        self.set_objectives(self._objectives)
        super().__init__(size, types, min_group)

    def _construct_tile(self, type, position, *args, **kwargs):
        """(LuckyTile) Returns a new tile from the generator's selection.

        Parameters:
            type (*): The type of the tile.
            position (tuple<int, int>): The position the tile will initially exist in. Unused.
            *args: Extra positional arguments for the tile.
            **kwargs: Extra keyword arguments for the tile.
        """
        return ObjectiveTile(type, *args, **kwargs)

    def check_objectives(self):
        objective = []
        for group in self.grid.find_all_connected():
            for position in group:
                cell = self.grid[position]
                for type, value in self.get_objectives():
                    #print("obj|", type, "in-grid|", cell.get_type(), "obj|", value, "in-grid|", cell.get_value())
                    if type == cell.get_type() and value <= cell.get_value():
                        #print("------------> type eq", type, cell.get_type())
                        #print("------------> val eq", value, cell.get_value())
                        #print("objective completed for", type, value)
                        objective.append((type, value))
                        if len(objective) > 0:
                            #print("remain", set(self.get_objectives()) - set(objective))
                            return set(self.get_objectives()) - set(objective)
        return self.get_objectives()

    def activate(self, position):
        self._moves_remaining -= 1
        #print(self.check_objectives())
        self.set_objectives(self.check_objectives())
        return game_regular.RegularGame.activate(self, position)

    @classmethod
    def set_objectives(cls, objectives):
        cls.OBJECTIVES = objectives

    @classmethod
    def get_objectives(cls):
        return cls.OBJECTIVES

    def get_moves_remaining(self):
        return self._moves_remaining

    def set_moves_remaining(self, moves):
        self._moves_remaining = moves

    def game_over(self):
        if self.get_moves_remaining() == 0:
            return True