from typing import Callable, List

from .fill_grid import fill_grid_dummy
from .grid import Cell, Grid
from .utils import Point2D


class GridManager:
    """
    Manages a grid and provides convenience access methods.
    """

    def __init__(self, grid_x: int = 10, grid_y: int = 10):
        self._grid = Grid(Point2D(grid_x, grid_y))
        self.nbr_mines = 0

    # GETTERS
    def get_grid_for_display(self) -> List[str]:
        return [self._cell_to_string(cell) for cell in self._grid]

    def get_cell_has_mine(self, cell_coord: Point2D) -> bool:
        return self._grid.get_cell_has_mine(cell_coord)

    def get_count_of_not_revealed_cells(self) -> int:
        return len([cell for cell in self._grid if not cell.is_revealed])

    def _cell_to_string(self, cell: Cell) -> str:
        if cell.is_revealed:
            if cell.has_mine:
                return "M"
            else:
                neighbours = self._grid.get_nb_of_close_mines(cell.pos)
                return str(neighbours)
        elif cell.is_flagged:
            return "F"
        else:
            return " "

    # UNITARY SETTERS
    def toggle_flag_cell(self, cell_coord: Point2D) -> None:
        cell = self._grid[cell_coord.x, cell_coord.y]
        if not cell.is_revealed:
            self._grid.set_cell_flagged(cell_coord, not cell.is_flagged)

    def _set_cell_has_mine(self, cell_coord: Point2D) -> None:
        self._grid[cell_coord.x, cell_coord.y].has_mine = True

    # GLOBAL MODIFIERS
    def fill_with_mines(
        self,
        nbr_mines: int = 3,
        procedure: Callable[[Callable[[Point2D], None],
                             int], None] = fill_grid_dummy
    ) -> None:
        self.nbr_mines = nbr_mines

        procedure(self._set_cell_has_mine, nbr_mines)

        assert len([cell for cell in self._grid if cell.has_mine]) == self.nbr_mines, \
            "Unexpected number of cells with a mine after filling the grid!"

    def reveal_all(self) -> List[str]:
        for cell in self._grid:
            cell.is_revealed = True
        return self.get_grid_for_display()

    class CellRevealer:
        def __init__(self, grid: Grid) -> None:
            self.grid = grid
            self.explored_no_neighbours = set()

        def run(self, cell_coord: Point2D) -> None:
            self.explored_no_neighbours.add(cell_coord)
            self.grid.set_cell_revealed(cell_coord, True)

            local_neighbours = self.grid.get_neighbours(cell_coord)
            for neighbour_cell in local_neighbours:
                neighbour_cell_pos = neighbour_cell.pos

                if neighbour_cell_pos in self.explored_no_neighbours:
                    continue

                if self.grid.get_nb_of_close_mines(neighbour_cell_pos) == 0:
                    self.run(
                        cell_coord=neighbour_cell_pos)
                else:
                    self.grid.set_cell_revealed(neighbour_cell_pos, True)

    def reveal_cell(self, cell_coord: Point2D) -> None:
        cell = self._grid[cell_coord.x, cell_coord.y]
        if not cell.is_revealed and not cell.is_flagged:
            self._grid.set_cell_revealed(cell_coord, True)
        if not cell.has_mine and self._grid.get_nb_of_close_mines(cell_coord) == 0:
            self.CellRevealer(grid=self._grid).run(cell_coord=cell_coord)