from PIL import Image, ImageTk
import tkinter as tk
# from pages.page1 import Page1 # Bỏ comment nếu bạn cần dùng
# from pages.page2 import Page2
# from pages.page3 import Page3
import time

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chia bố cục theo tỷ lệ")
        self.geometry("1680x960")

        self.init_menu() # Giữ lại nếu bạn có menu

        # Cấu hình trọng số cho các cột của cửa sổ chính (self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=1)
        # Cấu hình trọng số cho hàng của cửa sổ chính để các khung mở rộng theo chiều cao
        self.grid_rowconfigure(0, weight=1) 

        # Trái - Tương tác
        left_frame = tk.Frame(self, bg="lightgray")
        left_frame.grid(row=0, column=0, sticky="nsew")
        # --- Bỏ các dòng cấu hình trọng số bên trong khung con này ---
        # left_frame.grid_rowconfigure(0, weight=1)
        # left_frame.grid_columnconfigure(0, weight=1)
        
        # Thêm một nhãn để dễ nhìn thấy kích thước khung
        tk.Label(left_frame, text="Khung Trái (Tỷ lệ 1)", bg="lightgray").pack(expand=True, fill="both")


        # Giữa - Hiện ảnh
        mid_frame = tk.Frame(self, bg='lightblue')
        mid_frame.grid(row=0, column=1, sticky="nsew")
        # --- Bỏ dòng cấu hình trọng số bên trong khung con này ---
        # mid_frame.grid_columnconfigure(1, weight=8)
        
        # Thêm một nhãn để dễ nhìn thấy kích thước khung
        tk.Label(mid_frame, text="Khung Giữa (Tỷ lệ 8)", bg="blue", fg="white").pack(expand=True, fill="both")


        # Phải - Chỉ số thống kê
        right_frame = tk.Frame(self, bg="white")
        right_frame.grid(row=0, column=2, sticky="nsew")
        # --- Bỏ dòng cấu hình trọng số bên trong khung con này ---
        # right_frame.grid_columnconfigure(2, weight=1)
        
        # Thêm một nhãn để dễ nhìn thấy kích thước khung
        tk.Label(right_frame, text="Khung Phải (Tỷ lệ 1)", bg="white").pack(expand=True, fill="both")

    def init_menu(self):
        # Hàm khởi tạo menu của bạn (nếu có)
        pass

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()