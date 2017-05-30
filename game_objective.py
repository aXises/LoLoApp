"""Modelling classes for Lucky 7 Lolo game mode."""

import game_regular
import game_make13
import model
import tile_generators
from modules.weighted_selector import WeightedSelector
from random import randint

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
        self._type = type
        super().__init__(type, value)

        self._value = value
        self._objective_type = randint(1, 3)
        self._objective_value = "obj"

        objectives = ObjectiveGame.OBJECTIVES
        objective_chance = randint(1,10)
        print(ObjectiveGame.GENERATE_OBJECTIVES)
        while objectives < 5 and ObjectiveGame.GENERATE_OBJECTIVES:
            if objectives != 1 and objective_chance == 5:
                self.convert_objective()
                objectives += 1
            else:
                break

        print(ObjectiveGame.OBJECTIVES)



    def join(self, others):
        if self.get_value() == "obj":
            #print("clicked obj tile which is joinable")
            self.set_value(others[0].get_value())
        else:
            for other in others:
                if other.get_value() == "obj":
                    #print('joined objective tile')
                    pass

    def convert_objective(self):
        self._type = self._objective_type
        self._value = self._objective_value
        ObjectiveGame.OBJECTIVES += 1

    def set_value(self, value):
        self._value = value


class ObjectiveGame(game_regular.RegularGame):

    GAME_NAME = "Objective"
    OBJECTIVES = 0
    GENERATE_OBJECTIVES = True

    def __init__(self, size=(6,6), types=3, min_group=3, objective_value="obj",
                 objective_type=13, normal_weight=20, max_weight=2):

        # Basic properties
        self._objective_type = objective_type
        self._objective_value = objective_value
        super().__init__(size, types, min_group)
        if not self._resolving:
            self.find_obj_tiles()

    def get_default_score(self):
        """(int) Returns the default score."""
        return 0

    def _construct_tile(self, type, position, *args, **kwargs):
        """(LuckyTile) Returns a new tile from the generator's selection.

        Parameters:
            type (*): The type of the tile.
            position (tuple<int, int>): The position the tile will initially exist in. Unused.
            *args: Extra positional arguments for the tile.
            **kwargs: Extra keyword arguments for the tile.
        """
        return ObjectiveTile(type, *args, **kwargs)

    def find_obj_tiles(self):
        obj_tiles = 0
        for group in self.find_groups():
            for position in group:
                cell = self.grid[position]
                for neighbour in filter(None,
                                        self.grid.get_adjacent_cells(position)):
                    if neighbour in group:
                        print(position, cell.get_value())
                        if cell.get_value() == "obj":
                            obj_tiles += 1
        print(obj_tiles)
        ObjectiveGame.OBJECTIVES = obj_tiles

    def activate(self, position):
        test = True
        while not self._resolving and test == True:
            self.find_obj_tiles()
            test = False
        #print(self.find_obj_tiles())
        return game_regular.RegularGame.activate(self, position)
