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
<<<<<<< HEAD
        for other in others:
            if isinstance(other.get_value(), int):
                self._value += other.get_value()
        if self._value > 10:
            print("greater then 10")
=======
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
>>>>>>> parent of 7f0fd7e... Objective game mode (test)

    def set_value(self, value):
        self._value = value


class ObjectiveGame(game_regular.RegularGame):

    GAME_NAME = "Objective"
    OBJECTIVES = 0
    GENERATE_OBJECTIVES = True

    def __init__(self, size=(6,6), types=3, min_group=2, objective_value="obj",
                 objective_type=13, normal_weight=20, max_weight=2):

        # Basic properties
        self._objective_type = objective_type
        self._objective_value = objective_value
<<<<<<< HEAD
        self._updated_current_obj = False
        self._objective_to_remove = []
        self._moves_remaining = 50
=======
>>>>>>> parent of 7f0fd7e... Objective game mode (test)
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
<<<<<<< HEAD
        objectives = []
        id = 0
        for group in self.grid.find_all_connected():
            for position in group:
                cell = self.grid[position]
                if type(cell.get_value()) == str:
                    #print("found obj at", position)
                    objectives.append((cell, id))
                    id += 1
        return objectives

    def find_groups(self):
        objective = []
        for group in self.grid.find_all_connected():
            for position in group:
                cell = self.grid[position]
                print(cell.get_value())
                if type(cell.get_value()) == str:
                    objective.append(position)
            if len(group) < self.min_group:
                continue
            intersect = group - set(objective)
            #print("test")
            yield intersect

    def find_connections(self):
        connections = []
        for group in self.find_groups():
            for position in group:
                cell = self.grid[position]
                for neighbour in filter(None,
                                        self.grid.get_adjacent_cells(position)):
                    if neighbour in group:
                        connections.append(
                            (position, cell.get_type(), neighbour))
        print(connections)
        return connections

    def get_removed(self):
        current_objectives = a3.ObjectivesBar.get_objectives()
        in_grid_objectives = self.find_obj_tiles()
        in_grid_id = []
        # print("found", self.find_obj_tiles())
        # print("current are", current_objectives)
        for in_grid_objective, id in in_grid_objectives:
            in_grid_id.append(id)

        #print("current", current_objectives)
        #print("in grid", in_grid_objectives)

        for current_objective, id in current_objectives:
            if id not in in_grid_id:
                #print("not in", current_objective)
                if id not in self._objective_to_remove:
                    self._objective_to_remove.append(id)
        #print(self._objective_to_remove)
        return self._objective_to_remove


    def activate(self, position):
        self._moves_remaining -= 1
        remove_label = self.get_removed()
        #if len(remove_label) != 0:
            #a3.ObjectivesBar.destory_objective_label()

        if self.grid[position].get_value() == "obj":
            connected_cells = self._attempt_activate_collect(position)
            connected_cells.remove(position)
            for cell in connected_cells:
                del self.grid[cell]
            return game_regular.RegularGame.remove(self, position)
        else:
            return game_regular.RegularGame.activate(self, position)

    def reset(self):

        super().reset()
        self.convert_objective()

    def get_moves_remaining(self):
        return self._moves_remaining

    def set_moves_remaining(self, moves):
        self._moves_remaining = moves

    def game_over(self):
        if self.get_moves_remaining() == 0:
            return True

=======
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
>>>>>>> parent of 7f0fd7e... Objective game mode (test)
