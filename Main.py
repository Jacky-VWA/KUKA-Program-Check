# main_program.py

import logging
import tkinter as tk
from tkinter import filedialog, messagebox
from check_specifical_files import CheckSpecificalFiles
from check_makro_files import CheckMakroFiles

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KUKA机器人程序检查工具")

        self.select_button = tk.Button(root, text="选择文件", command=self.select_files)
        self.select_button.pack(pady=10)

        self.select_template_button = tk.Button(root, text="选择模板文件", command=self.select_template_file)
        self.select_template_button.pack(pady=10)

        self.check_button = tk.Button(root, text="开始检查", command=self.check_files, state=tk.DISABLED)
        self.check_button.pack(pady=10)

        self.zip_files = []
        self.template_file = None

    def select_files(self):
        self.zip_files = filedialog.askopenfilenames(filetypes=[("ZIP files", "*.zip")])
        if self.zip_files:
            self.check_button.config(state=tk.NORMAL)
        else:
            self.check_button.config(state=tk.DISABLED)

    def select_template_file(self):
        self.template_file = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])

    def check_files(self):
        # 特定文件检查
        specifical_checker = CheckSpecificalFiles()
        result_specifical, found_files_specifical = specifical_checker.run(self.zip_files)

        # Makro 文件检查
        makro_checker = CheckMakroFiles()
        result_makro, found_files_makro, inconsistent_files_makro = makro_checker.run(
            self.zip_files,
            template_file=self.template_file  # 默认使用模板文件
        )

        # 存储结果到各自的变量中
        self.results = {
            "特定文件检查": (result_specifical, found_files_specifical),
            "Makro 文件检查": (result_makro, found_files_makro)
        }

        # 显示所有检查结果
        self.show_results()

    def show_results(self):
        for check_name, (result, found_files) in self.results.items():
            if result:
                found_files_str = "\n".join(found_files.keys()) if isinstance(found_files, dict) else "无"
                messagebox.showinfo(f"{check_name} 结果", f"找到匹配的文件：\n{found_files_str}")
            else:
                messagebox.showinfo(f"{check_name} 结果", "没有找到匹配的文件。")

# 创建主窗口
if __name__ == "__main__":
    # 设置 NumExpr 的最大线程数
    import numexpr as ne
    ne.set_num_threads(8)  # 设置最大线程数
    ne.use_vml = False  # 禁用 VML 支持（可选）

    root = tk.Tk()
    app = FileCheckerApp(root)
    root.mainloop()