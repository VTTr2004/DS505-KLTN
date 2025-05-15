import tkinter as tk
from tkinter import filedialog
import subprocess

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Quản Lý Camera", font=("Arial", 18))\
        .grid(column = 0, row = 0, sticky = 'w')

        tk.Button(self, text = 'Chọn Cam 1', command = self.Choose_Video)\
        .grid(column = 0, row = 1, sticky = 'w')

        tk.Button(self, text = 'Chọn Cam 2', command = self.Choose_Video)\
        .grid(column = 0, row = 2, sticky = 'w')

    @staticmethod
    def Choose_Video():
        file_path = filedialog.askopenfilename(
            title="Chọn file video",
            filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov *.wmv"), ("All files", "*.*")]
        )
        if file_path:
            print("Đã chọn video:", file_path)

        subprocess.run([
            "python", 
            "E:\\GitHUB\\Traffic_Violation\\sender.py", 
            "--file", 
            file_path
        ])