import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Toplevel
from tkinter import ttk
import cv2
import os

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("车辆零部件表面缺陷检测系统")
        self.geometry("800x600")
        self.create_widgets()
        self.images = []

    def create_widgets(self):
        # 主界面
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.image_label = ttk.Label(self.main_frame, text="欢迎使用车辆零部件表面缺陷检测系统")
        self.image_label.pack(pady=20)

        self.image_button = ttk.Button(self.main_frame, text="导入图像", command=self.import_image)
        self.image_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.camera_button = ttk.Button(self.main_frame, text="拍摄图像", command=self.capture_image)
        self.camera_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.manage_button = ttk.Button(self.main_frame, text="管理", command=self.manage)
        self.manage_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.user_button = ttk.Button(self.main_frame, text="用户管理", command=self.user_management)
        self.user_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.report_button = ttk.Button(self.main_frame, text="报告生成", command=self.report_generation)
        self.report_button.pack(side=tk.LEFT, padx=10, pady=10)

    def import_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.images.append(file_path)
            messagebox.showinfo("信息", f"已选择文件: {file_path}")
            self.update_image_list()

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("captured_image.jpg", frame)
            self.images.append("captured_image.jpg")
            messagebox.showinfo("信息", "拍摄图像成功")
            self.update_image_list()
        cap.release()

    def update_image_list(self):
        self.image_list_label = ttk.Label(self.main_frame, text="\n".join(self.images))
        self.image_list_label.pack()

    def manage(self):
        self.manage_window = Toplevel(self)
        self.manage_window.title("管理")
        self.manage_window.geometry("300x200")

        self.delete_button = ttk.Button(self.manage_window, text="删除", command=self.delete_image)
        self.delete_button.pack(pady=10)

    def delete_image(self):
        if self.images:
            image_to_delete = simpledialog.askstring("删除", "请输入要删除的图像文件名:")
            if image_to_delete in self.images:
                self.images.remove(image_to_delete)
                os.remove(image_to_delete)
                messagebox.showinfo("信息", "图像已删除")
                self.update_image_list()
            else:
                messagebox.showwarning("警告", "文件名不正确或文件不存在")
        else:
            messagebox.showwarning("警告", "没有图像可删除")

    def user_management(self):
        self.user_window = Toplevel(self)
        self.user_window.title("用户管理")
        self.user_window.geometry("300x200")

        self.login_label = ttk.Label(self.user_window, text="用户名:")
        self.login_label.pack()

        self.login_entry = ttk.Entry(self.user_window)
        self.login_entry.pack()

        self.login_button = ttk.Button(self.user_window, text="登录", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        username = self.login_entry.get()
        messagebox.showinfo("信息", f"登录用户: {username}")

    def report_generation(self):
        self.report_window = Toplevel(self)
        self.report_window.title("报告生成")
        self.report_window.geometry("400x300")

        self.preview_button = ttk.Button(self.report_window, text="预览报告", command=self.preview_report)
        self.preview_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.export_button = ttk.Button(self.report_window, text="导出报告", command=self.export_report)
        self.export_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.manage_report_button = ttk.Button(self.report_window, text="管理报告", command=self.manage_report)
        self.manage_report_button.pack(side=tk.LEFT, padx=10, pady=10)

    def preview_report(self):
        report_text = "报告预览\n" + "\n".join(self.images)
        messagebox.showinfo("报告预览", report_text)

    def export_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                for image in self.images:
                    file.write(image + "\n")
            messagebox.showinfo("信息", f"报告已保存到: {file_path}")

    def manage_report(self):
        report_text = "已生成报告列表:\n" + "\n".join(self.images)
        messagebox.showinfo("管理报告", report_text)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
