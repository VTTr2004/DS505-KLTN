from PIL import Image, ImageTk
import tkinter as tk
from pages.page1 import Page1
from pages.page2 import Page2
from pages.page3 import Page3

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chia bố cục theo tỷ lệ")
        self.geometry("1000x650")

        self.init_menu()

        self.grid_columnconfigure(0, weight=3)  # 30%
        self.grid_columnconfigure(1, weight=7)  # 70%
        self.grid_rowconfigure(0, weight=1)

        # Vùng trang (trái)
        left_frame = tk.Frame(self, bg="lightgray")
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Page1, Page2, Page3):
            page_name = F.__name__
            frame = F(parent=left_frame, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Page1")

        # Vùng ảnh (phải)
        right_frame = tk.Frame(self, bg="white")
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Hiển thị ảnh
        image = Image.open("./MaiChiTho_cam_1_7.jpg")
        # image = image.resize((700, 500))
        self.tk_image = ImageTk.PhotoImage(image)
        img_label = tk.Label(right_frame, image=self.tk_image)
        img_label.pack(pady=10)
        img_label = tk.Label(right_frame, image=self.tk_image)
        img_label.pack(pady=0)

    def init_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        menubar.add_command(label="Trang 1", command=lambda: self.show_frame("Page1"))
        menubar.add_command(label="Trang 2", command=lambda: self.show_frame("Page2"))
        menubar.add_command(label="Trang 3", command=lambda: self.show_frame("Page3"))

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
