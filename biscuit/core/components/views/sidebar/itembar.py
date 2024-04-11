import tkinter as tk

from biscuit.core.utils import Frame, IconButton


class ItemBar(Frame):
    def __init__(self, master, title=None, buttons=(), *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.config(**self.base.theme.views.sidebar.itembar)

        self.grid_columnconfigure(1, weight=1)

        self.title = tk.StringVar()
        if title:
            self.set_title(title)

        self.toggle = IconButton(self, icon='chevron-down', event=self.toggle_content, width=1)
        self.toggle.grid(row=0, column=0)

        self.label_title = tk.Label(self, anchor=tk.W, textvariable=self.title, font=("Segoi UI", 9, "bold"),  **self.base.theme.views.sidebar.itembar.title)
        self.label_title.grid(row=0, column=1, sticky=tk.EW)

        self.buttoncolumn = 0
        self.buttonframe = Frame(self,  **self.base.theme.views.sidebar.itembar)
        self.buttonframe.grid(row=0, column=2, sticky=tk.E)

        self.add_buttons(buttons)

    def add_button(self, *args) -> None:
        IconButton(self.buttonframe, *args).grid(row=0, column=self.buttoncolumn)
        self.buttoncolumn += 1

    def add_buttons(self, buttons) -> None:
        for btn in buttons:
            self.add_button(*btn)

    def set_title(self, title) -> None:
        self.title.set(title.upper())

    def toggle_content(self, *_) -> None:
        if not self.master.enabled:
            self.toggle.set_icon('chevron-down')
        else:
            self.toggle.set_icon('chevron-right')
        self.master.toggle()

    def hide_content(self, *_) -> None:
        self.toggle.set_icon('chevron-right')
        self.master.disable()

    def show_content(self, *_) -> None:
        self.toggle.set_icon('chevron-down')
        self.master.enable()
