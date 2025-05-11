import tkinter as tk

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Đây là Trang 2", font=("Arial", 18)).pack(pady=20)