from dataclasses import dataclass
from enum import Enum
from typing import Optional

from view.gui import GUI


@dataclass(frozen=True)
class DifficultyLevel:
    """
    A level of difficulty is defined by the grid size and the number of mines.
    """
    nbr_mines: int
    grid_x: int
    grid_y: int


class DifficultyLevels(Enum):
    """
    Enumeration of known difficulty levels.
    """
    EASY = DifficultyLevel(nbr_mines=10, grid_x=8, grid_y=8)
    INTERMEDIATE = DifficultyLevel(nbr_mines=40, grid_x=16, grid_y=16)
    EXPERT = DifficultyLevel(nbr_mines=99, grid_x=30, grid_y=16)


class Controller:
    def init_gui(self, gui: GUI) -> None:
        raise NotImplementedError()

    def on_new_game(self, difficulty_level: Optional[DifficultyLevel] = None) -> None:
        raise NotImplementedError()

    def on_left_click(self, cell_x: int, cell_y: int) -> None:
        raise NotImplementedError()

    def on_right_click(self, x: int, y: int) -> None:
        raise NotImplementedError()

    def get_nbr_mines(self) -> int:
        raise NotImplementedError()

    def get_game_starting_time(self) -> float:
        raise NotImplementedError()
