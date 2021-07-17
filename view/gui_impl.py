import time
import tkinter as tk
from typing import List

from overrides import overrides

from controller.controller import Controller
from game_engine.utils import Point2D
from .controls import ControlsWidget
from .grid import GridView
from .gui import GUI


WIN_WIDTH = 500


class GUIImpl(GUI):
    def __init__(
            self,
            grid_x: int, grid_y: int,
            controller: Controller = None,) -> None:
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Mfranceschi Minesweeper!")

        self.elapsed_time_text = tk.StringVar(master=self.root, value="")
        self._update_elapsed_time_text()

        self.grid_frame = self.GridFrame(self)
        self.grid_frame.grid(column=0, row=0)

        self.bottom_frame = self.ControlsWidget(self)
        self.bottom_frame.grid(column=0, row=1)

    @overrides
    def set_grid(self, grid: List[str]) -> None:
        self.grid_frame.set_grid(grid)

    def on_left_click_on_cell(self, cell_coord: Point2D):
        self.controller.on_left_click(cell_coord)

    def on_right_click_on_cell(self, cell_coord: Point2D):
        self.controller.on_right_click(cell_coord)

    def _update_elapsed_time_text(self):
        elapsed_seconds = time.time() - self.controller.get_game_starting_time()
        minutes, seconds = divmod(int(elapsed_seconds), 60)
        self.elapsed_time_text.set(
            f"Elapsed time: {f'{minutes}min ' if minutes else ''}{seconds}s")
        self.root.after(800, self._update_elapsed_time_text)

    @overrides
    def reset_grid_size(self, grid_x: int, grid_y: int) -> None:
        self.grid_frame.destroy()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_frame = self.GridFrame(self)
        self.grid_frame.grid(row=0, column=0)

    @overrides
    def set_nbr_mines(self, nbr_mines: int) -> None:
        self.bottom_frame.set_nbr_mines(nbr_mines)

    @overrides
    def victory(self) -> None:
        self.root.configure(bg="green")

    @overrides
    def game_over(self) -> None:
        self.root.configure(bg="brown")

    @overrides
    def game_starts(self) -> None:
        self.root.configure(bg="sky blue")

    class GridFrame(GridView):
        """
        An easier-to-configure GridView.
        """

        def __init__(self, gui_impl, *args, **kwargs) -> None:
            super().__init__(
                master=gui_impl.root,
                height=WIN_WIDTH,
                bg="red",

                size_x=gui_impl.grid_x,
                size_y=gui_impl.grid_y,
                on_left_click=gui_impl.on_left_click_on_cell,
                on_right_click=gui_impl.on_right_click_on_cell,
                *args, **kwargs
            )

    class ControlsWidget(ControlsWidget):
        """
        An easier-to-configure ControlsWidget.
        """

        def __init__(self, gui_impl, *args, **kwargs):
            super().__init__(
                master=gui_impl.root,
                height=30,
                bg="blue",

                controller=gui_impl.controller,
                elapsed_time_text=gui_impl.elapsed_time_text,

                *args, **kwargs
            )
