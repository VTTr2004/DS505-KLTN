import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

def upload_video():
    path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])
    status_label.config(text=f"Video đã chọn: {path}")

root = tk.Tk()
root.title("Ứng dụng xử lý video")
root.geometry("800x600")

# Phần đầu – chọn file
top_frame = tk.Frame(root, height=100, bg="lightgray")
top_frame.pack(fill="x")
upload_btn = tk.Button(top_frame, text="Chọn video", command=upload_video)
upload_btn.pack(pady=20)

# Phần giữa – hiển thị trạng thái
middle_frame = tk.Frame(root, height=250, bg="white")
middle_frame.pack(fill="x")
status_label = tk.Label(middle_frame, text="Chưa chọn video", fg="blue")
status_label.pack(pady=50)

# Phần cuối – hiển thị ảnh
bottom_frame = tk.Frame(root, bg="lightblue")
bottom_frame.pack(fill="both", expand=True)
# Ở đây bạn có thể dùng Label + ImageTk.PhotoImage để hiện ảnh xử lý

root.mainloop()