# file_importer.py

import zipfile
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def import_zip(zip_file):

    if not zip_file:
        print("未选择文件。")
        return []

    extracted_files = []
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall("extracted_files")  # 提取到指定文件夹
            extracted_files = zip_ref.namelist()  # 获取文件列表
            print(f"成功导入 ZIP 文件：{zip_file}")
            print(f"提取的文件：{extracted_files}")
    except zipfile.BadZipFile:
        print("错误：无效的 ZIP 文件。")
    except Exception as e:
        print(f"发生错误：{e}")

    return extracted_files
