import logging
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import os
from datetime import datetime
from check_specifical_files import CheckSpecificalFiles
from check_makro_files import CheckMakroFiles
from check_user_files import CheckUserFiles  # 导入新的检查类

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KUKA机器人程序检查工具")
        self.root.geometry("500x400")  # 设置窗口大小为 500x400 像素
        
        # 创建样式
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 使用更现代的主题
        
        # 设置按钮和标签的样式
        self.style.configure("TButton", padding=10, font=("Arial", 12), background="#4CAF50", foreground="white")  # 按钮样式
        self.style.configure("TLabel", font=("Arial", 12))  # 标签样式
        
        # 设置窗口背景颜色
        self.root.configure(bg="#f0f0f0")  # 设置对话框背景色

        # 创建按钮
        self.select_button = ttk.Button(root, text="选择文件", command=self.select_files)
        self.select_button.pack(pady=20)

        self.select_template_button = ttk.Button(root, text="选择模板文件", command=self.select_template_file)
        self.select_template_button.pack(pady=20)

        self.check_button = ttk.Button(root, text="开始检查", command=self.check_files, state=tk.DISABLED)
        self.check_button.pack(pady=20)

        self.zip_files = []
        self.template_file = None

    def select_files(self):
        """选择ZIP文件"""
        try:
            self.zip_files = filedialog.askopenfilenames(filetypes=[("ZIP files", "*.zip")])
            if self.zip_files:
                logging.info(f"选择了 {len(self.zip_files)} 个文件。")
                self.check_button.config(state=tk.NORMAL)
            else:
                self.check_button.config(state=tk.DISABLED)
        except Exception as e:
            logging.error(f"选择文件时出错: {e}")
            messagebox.showerror("错误", "选择文件时发生错误。")

    def select_template_file(self):
        """选择模板文件"""
        try:
            self.template_file = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
            if self.template_file:
                logging.info(f"选择了模板文件: {self.template_file}")
        except Exception as e:
            logging.error(f"选择模板文件时出错: {e}")
            messagebox.showerror("错误", "选择模板文件时发生错误。")

    def check_files(self):
        """执行文件检查"""
        try:
            self.check_button.config(state=tk.DISABLED)

            # 存储所有检查结果
            self.results = {}

            for zip_file in self.zip_files:
                # 特定文件检查
                specifical_checker = CheckSpecificalFiles()
                result_specifical, found_files_specifical = specifical_checker.run([zip_file])

                # Makro 文件检查
                makro_checker = CheckMakroFiles()
                result_makro, found_files_makro, inconsistent_files_makro = makro_checker.run(
                    [zip_file],
                    template_file=self.template_file
                )

                # 用户文件检查
                user_checker = CheckUserFiles()
                result_user, found_files_user = user_checker.run([zip_file], template_file=self.template_file)

                # 存储结果到字典
                self.results[os.path.basename(zip_file)] = {
                    "特定文件检查": (result_specifical, found_files_specifical),
                    "Makro 文件检查": (result_makro, found_files_makro, inconsistent_files_makro),
                    "用户文件检查": (result_user, found_files_user)
                }

            # 保存结果到 Excel
            self.save_results_to_excel()

        except Exception as e:
            logging.error(f"检查文件时出错: {e}")
            messagebox.showerror("错误", "检查文件时发生错误。")
        finally:
            self.check_button.config(state=tk.NORMAL)

    def save_results_to_excel(self):
        """将检查结果保存到 Excel 文件"""
        # 创建 Excel 文件名
        current_date = datetime.now().strftime("%Y-%m-%d")
        excel_file_name = f"机器人程序检查结果_{current_date}.xlsx"

        # 创建一个 Excel Writer 对象
        with pd.ExcelWriter(excel_file_name, engine='openpyxl') as writer:
            for zip_file, checks in self.results.items():
                # 创建 DataFrame
                data = {
                    "检查类型": [],
                    "结果": [],
                    "找到的文件": []
                }

                for check_type, (result, *found_files) in checks.items():
                    data["检查类型"].append(check_type)
                    data["结果"].append(result)
                    data["找到的文件"].append(", ".join(found_files[0]))

                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=os.path.basename(zip_file), index=False)

        logging.info(f"检查结果已保存到 {excel_file_name}。")
        messagebox.showinfo("完成", f"检查结果已保存到 {excel_file_name}。")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCheckerApp(root)
    root.mainloop()
