import tkinter as tk
from typing import Any, Callable

from controller.controller import Controller, DifficultyLevel, DifficultyLevels


class NewGameButton(tk.Button):
    """
    Wraps a button. On click, calls the given command to start a new game.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(background="yellow", *args, **kwargs)
        self.grid(row=0, column=0, columnspan=2)


class NbrMinesLabel(tk.Label):
    """
    Wraps a label with the number of mines.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=2, padx=20)

    @staticmethod
    def _make_string_for_nbr_mines(nbr: int) -> str:
        return f"There are {nbr} mines!"

    def set_nbr_mines(self, nbr: int) -> None:
        self.configure(text=self._make_string_for_nbr_mines(nbr))


class DifficultyChoice(tk.Frame):
    """
    Wraps a frame that allows the user to select a difficulty
    and start a new game with it.
    """

    def __init__(
        self,
        on_new_difficulty: Callable[[DifficultyLevel], None],
        *args: Any, **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.on_new_difficulty = on_new_difficulty
        self.grid(row=0, column=3, padx=20)

        self.listbox = tk.Listbox(
            master=self, selectmode=tk.SINGLE, width=0, height=0)
        choices = [x.name.title() for x in DifficultyLevels]
        self.listbox.insert(tk.END, *choices)
        self.listbox.selection_anchor(0)
        self.listbox.pack()

        self.ok_button = tk.Button(
            master=self, text="OK (new game)", command=self._handle_ok)
        self.ok_button.pack()

    def _handle_ok(self):
        choice: str = str(self.listbox.get(tk.ANCHOR)).upper()
        assert choice in DifficultyLevels.__members__.keys()
        self.on_new_difficulty(getattr(DifficultyLevels, choice).value)


class ElapsedTimeLabel(tk.Label):
    """
    Wraps a label with the elapsed time, straight from the text variable.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid(row=0, column=4)


class ControlsWidget(tk.Frame):
    """
    Wraps some cool widgets that display stuff or provide the user with input items.
    """

    def __init__(self, controller: Controller, elapsed_time_text: tk.StringVar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padx=15, pady=15, background="white")

        self.new_game_button = NewGameButton(
            master=self, command=controller.on_new_game, text="New game")

        self.nbr_mines_label = NbrMinesLabel(master=self)
        self.nbr_mines_label.set_nbr_mines(controller.get_nbr_mines())

        self.difficulty_choice = DifficultyChoice(
            master=self, on_new_difficulty=controller.on_new_game)

        self.elapsed_time_label = ElapsedTimeLabel(
            master=self, textvariable=elapsed_time_text)

    def set_nbr_mines(self, nbr: int) -> None:
        self.nbr_mines_label.set_nbr_mines(nbr)
