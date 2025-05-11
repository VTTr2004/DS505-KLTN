import subprocess
import os
import tkinter as tk

    
class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        tk.Label(self, text="Quản Lý Kafka", font=("Arial", 18))\
        .grid(row=0, column=0)

        tk.Button(self, text = "Chạy Kafka", command = self.Start_Kafka_Server)\
        .grid(row=1, column=0, sticky="w")

        tk.Label(self, text="Tạo topic", font=("Arial", 12))\
        .grid(row=2, column=0, sticky="w")

        tk.Label(self, text="Nhập topic-port (topic_1-local):")\
        .grid(row=3, column=0, sticky="w")
        entry = tk.Entry(self, width=30)
        entry.grid(row=3, column=1, sticky='w')
        tk.Button(self, text = "Tạo", command = lambda: self.Create_Topic(entry.get()))\
        .grid(row=4, column=0, sticky="w")

        tk.Label(self, text="Nhập port:")\
        .grid(row=5, column=0, sticky="w")
        entry_2 = tk.Entry(self, width=10)
        entry_2.grid(row=5, column=1, sticky='w')
        tk.Button(self, text = "Danh sách topic", command = lambda: self.List_Topic(entry_2.get()))\
        .grid(row=6, column=0, sticky="w")

        tk.Label(self, text="Quản Lý Spark", font=("Arial", 18))\
        .grid(row=8, column=0)
        tk.Button(self, text = "Chạy Spark", command = self.Run_Spark)\
        .grid(row=9, column=0, sticky="w")

        tk.Label(self, text="Quản Lý Output", font=("Arial", 18))\
        .grid(row=10, column=0)
        tk.Button(self, text = "Chạy Output", command = self.Run_Output)\
        .grid(row=11, column=0, sticky="w")

    @staticmethod
    def Start_Kafka_Server():
        subprocess.Popen(
            'start cmd /k "C: && \
            cd \\kafka_2.13-4.0.0 && \
            bin\\windows\\kafka-server-start.bat config\\server.properties"',
            shell=True
        )

    @staticmethod
    def Create_Topic(data):
        temp = data.split("-")
        topic = temp[0]
        port = temp[1]
        command = [
            'C:\\kafka_2.13-4.0.0\\bin\\windows\\kafka-topics.bat',
            '--create',
            '--topic', topic,
            '--bootstrap-server', f'localhost:{port}',
            # '--partitions', '1',
            # '--replication-factor', '1'
        ]
        
        subprocess.run(command)
    
    def List_Topic(self, port):
        command = [
            'C:\\kafka_2.13-4.0.0\\bin\\windows\\kafka-topics.bat',
            '--list',
            '--bootstrap-server',
            f'localhost:{port}',
        ]
        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        text_widget = tk.Text(self, height=5, width=30)
        text_widget.insert("1.0", " ".join(result.stdout.split("\n")[1:]))
        text_widget.config(state="disabled")  # Không cho người dùng sửa
        text_widget.grid(row=7, column=0, sticky="w", columnspan=2)

    @staticmethod
    def Run_Spark():
        file_path = os.path.join("E:\\GitHUB\\Traffic_Violation", "consumer_cam.py")
        print(f'start cmd /k "python {file_path}"')

        subprocess.Popen(f'start cmd /k "python {file_path}"', shell=True)
        # subprocess.run(["python", file_path])

    @staticmethod
    def Run_Output():
        file_path = os.path.join("E:\\GitHUB\\Traffic_Violation", "consumer_output.py")
        print(f'start cmd /k "python {file_path}"')

        subprocess.Popen(f'start cmd /k "python {file_path}"', shell=True)
        # subprocess.run(["python", file_path])