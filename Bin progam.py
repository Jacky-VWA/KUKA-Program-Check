#导入用于检查Python包的功能，通常用于确保包的质量
from distutils.command.check import check
#导入队列模块中的Full异常，通常用于处理队列已满的情况
from queue import Full
#导入处理ZIP文件的模块，可以用于创建、读取、写入ZIP文件
import zipfile
#提供支持regular expressions, 用于define patterns
import re
#导入数学模块中的trunc函数，用于截断数字（去掉小数部分）
from math import trunc
# 导入Tkinter库，Python的标准GUI工具包，用于创建图形用户界面。
import tkinter as tk
# 从Tkinter中导入选择和文件对话框功能，用于文件选择
from tkinter import SEL, filedialog
#  导入操作系统相关的功能模块，提供与操作系统交互的功能
import os
# import time
# import filecmp
# 导入用于比较序列（如文件或字符串）的模块，常用于查找差异
import difflib
# import chardet
# import pandas as pd
# 导入高层次的文件操作模块，提供文件复制、删除等功能
import shutil
# 导入用于读取和写入Excel文件的库
import openpyxl
# 从openpyxl中导入字体样式功能，用于设置Excel单元格的字体样式。
from openpyxl.styles import Font
# 导入ttkbootstrap库，提供现代化的Tkinter应用程序样式A
import ttkbootstrap as ttk
# 从ttkbootstrap中导入样式功能，用于设置应用程序的外观
from ttkbootstrap import Style
# 导入时间模块，用于处理时间相关的功能
import time
# pattern2 = r'(?i)Makro(?!5[0-9]\.)\d+|usr_s|usr_r|makrostep|makrosps|makrosubmit|makrotrigger'
# 用于匹配特定字符串（如"makro"和"usr_s"等）
pattern2 = r'(?i)makro(?!5[0-9]\.)|usr_s|usr_r'
# 用于匹配以"Folge"或"Up"开头的文件名
pattern_folge_up = r'(Folge|Up)\d+\.dat'
# 用于匹配不以"U"开头的"P"后面跟数字的模式
pattern_n_folge_up = r'(?<!U) P(\d+)'
# 定义红色字体样式
red = Font(color='FF0000')
# 定义黑色字体样式
green = Font(color='000000')
# 以上代码为后续的程序逻辑提供了必要的库和工具，可能用于构建一个图形用户界面应用程序，处理文件和数据。


# 定义了一个名为 template_import 的函数，主要用于选择文件夹并查找特定类型的文件
def template_import():
    # 以下两句自锁
    # 使用 os.path.exists 检查路径 C:\Programing\system file\damage 是否存在。
    if os.path.exists(r'C:\Programing\system file\damage'):
        with open(full_path, 'r') as check_file:
            # 标志位自锁
            if 'invalid' in check_file.read():
                return self_damage
    else:
        return self_damage()

    # button1 = tk.Button(command=template_import)
    # button1.pack(pady=50)

    # 让用户选择文件夹
    global template_file_paths  # 将变量定义为全局变量
    # 使用 filedialog.askdirectory() 让用户选择一个文件夹，并将其路径存储在 template_folder_path 变量中
    template_folder_path = filedialog.askdirectory()

    # 遍历文件夹及其子目录，用于匹配以 .txt、.TXT、.dat 或 .src 结尾的文件
    pattern = ".*\.(txt|TXT|dat|src)"  # 只筛选出以".txt"结尾的文件名

    # 初始化两个全局变量：template_file_paths（存储找到的文件路径）
    template_file_paths = []
    template_name = []

    # 使用 os.walk 遍历用户选择的文件夹及其子目录，寻找符合条件的文件。
    # 在遍历过程中，对于每个文件名，使用 re.match 检查是否符合定义的模式。如果匹配，将文件的完整路径添加到 template_file_paths 列表中
    for dir_path, dir_names, file_names in os.walk(template_folder_path):
        # 遍历当前目录下的所有文件，找出所有txt文件
        # print (dir_path)
        # print(dir_names)
        # print(file_names)
        for file_name in file_names:
            # print (dir_path)
            # print('qwe'+file_name)
            if re.match(pattern, file_name):
                # print(file_name)
                # template_name.append(file_name)
                file_path = os.path.join(dir_path, file_name)
                # print(file_path)
                template_file_paths.append(file_path)
    # 所有模板文档都在template_file_names里
# 该函数的主要目的是让用户选择一个文件夹，然后在该文件夹及其子目录中查找所有以 .txt、.dat 或 .src 结尾的文件，并将它们的路径保存到一个全局列表中。
# 在执行文件查找之前，函数会检查特定路径的存在性和文件内容，以决定是否继续执行

# 定义了一个名为 target_import 的函数，主要用于处理压缩文件（ZIP），提取其中的特定数据，并将结果写入 Excel 文件
def target_import():
    # 以下两句自锁
    # 检查路径 C:\Programing\system file\damage 是否存在。如果存在，打开full_path 文件（可能是全局变量），检查内容是否包含字符串 'invalid'
    if os.path.exists(r'C:\Programing\system file\damage'):
        with open(full_path, 'r') as check_file:
            # 标志位自锁
            if 'invalid' in check_file.read():
                return self_damage
    else:
        return self_damage()
    # try:
    # global template_file_paths
    # 定义全局变量 target_file_paths、zip_damaged 和 text_read_failed，用于存储目标文件路径、损坏的ZIP文件列表、读取失败的文本文件列表
    global target_file_paths
    target_file_paths = []
    zip_damaged = []
    text_read_failed = []

    # 使用 filedialog.askopenfilenames() 弹出文件选择对话框，允许用户选择多个 ZIP 文件。选择的文件路径将存储在 R_filenames 列表中
    R_filenames = filedialog.askopenfilenames()
    # 计算所选文件的数量，并将其存储在 robot_number 变量中，然后打印出来
    robot_number = len(R_filenames)
    print(robot_number)

    # 初始化一个计数器 robot_checked，用于跟踪已处理的文件数量
    robot_checked = 0

    # print(template_file_paths)
    # 对于每个用户选择的 ZIP 文件，初始化一个空列表 target_file_paths，用于存储提取的目标文件路径。
    for R_filename in R_filenames:
        target_file_paths = []
        # 将 ZIP 文件的扩展名 .zip 替换为 .xlsx，生成对应的 Excel 文件名
        excel_name = R_filename.replace('.zip', '.xlsx')
        # print(excel_name)
        # 使用 shutil.copyfile() 将模板 Excel 文件复制到新生成的 Excel 文件名中
        shutil.copyfile(template_excel[0], excel_name)
        # 使用 openpyxl 库加载刚才创建的 Excel 文件
        workbook = openpyxl.load_workbook(excel_name)
        # print(workbook.sheetnames)
        # 获取工作簿中的四个工作表，分别用于存储不同类型的数据
        sheet_makros = workbook['Sheet1']
        sheet_usrs = workbook['Sheet2']
        sheet_folge_up = workbook['Sheet3']
        sheet_fault = workbook['Sheet4']
        n_makro = 4
        n_usr = 4
        n_folge_up = 4
        n_fault = 4
        # 以上这段代码的主要目的是为每个用户选择的 ZIP 文件创建一个新的 Excel 文件，并准备好工作表以供后续的数据提取和比较。
        # 通过这种方式，用户可以方便地管理和分析从 ZIP 文件中提取的数据


        try:
            with zipfile.ZipFile(R_filename, 'r') as myzip:
                # 使用 myzip.namelist() 获取 ZIP 文件中的所有文件名，并对每个文件名进行遍历
                for name in myzip.namelist():
                    # 使用 os.path.basename(name) 提取文件名（不包括路径），将其存储在 name_1 中
                    name_1 = os.path.basename(name)
                    # print(name)
                    # 使用正则表达式 pattern2 检查文件名是否符合特定模式。如果匹配，将文件名添加到 target_file_paths 列表中
                    if re.search(pattern2, name_1):
                        target_file_paths.append(name)
                        # print('qwe',name)
                    #     取出Folge125的P0点，检查当前文件是否为 KRC/R1/Folgen/Folge125.dat，如果是，则打开该文件进行处理。
                    if name=="KRC/R1/Folgen/Folge125.dat":
                            # print(name)
                        # 使用 myzip.open(name) 打开文件，并将其内容读取为 UTF-8 编码的字符串
                        with myzip.open(name) as myfile:
                            text=myfile.read().decode('utf-8')
                            # print(text)
                            # 通过 find() 方法查找 P0_D 和 P0 的起始和结束位置，以便提取相关数据。
                            P0_D_start = text.find("P0_D")
                            P0_D_start = text.find("{", P0_D_start)
                            P0_D_end = text.find("}", P0_D_start + 1)
                            P0_start = text.find("{", P0_D_end + 1)
                            P0_end = text.find("}", P0_start + 1)
                            P0_D_text = text[P0_D_start:P0_D_end + 1]
                            P0_text = text[P0_start:P0_end + 1]
                            # print('P0_D=',P0_D_text)
                            # 去除空格
                            P0_D_text = re.sub(r'\s+', '', P0_D_text)
                            P0_text = re.sub(r'\s+', '', P0_text)
                            # 除去VB
                            P0_D_text_de_VB=re.sub(r'VB\d+,', '', P0_D_text)

                            # print('P0=', P0_text)
                print(R_filename)
                print('target=',target_file_paths)
                print('template=', template_file_paths)

                # print(template_file_paths)
                for name in myzip.namelist():
                    folge_up_flag = True
                    if re.search(pattern_folge_up, name):
                        name_2 = os.path.basename(name)
                        sheet_folge_up[f'A{n_folge_up}'] = f'{name_2}'

                        # print(name)
                        # f.write('\n' + '\n' + '\n' + name + '\n')
                        with myzip.open(name) as myfile:
                            text_folge_up = myfile.read().decode('utf-8')
                       # 找出P1及其P1_D
                            P1_D_start = text_folge_up.find("P1_D")
                            P1_D_start = text_folge_up.find("{", P1_D_start)
                            P1_D_end = text_folge_up.find("}", P1_D_start + 1)
                            P1_start = text_folge_up.find("{", P1_D_end + 1)
                            P1_end = text_folge_up.find("}", P1_start + 1)
                            P1_D_text = text_folge_up[P1_D_start:P1_D_end + 1]

                            P1_text = text_folge_up[P1_start:P1_end + 1]
                            # print('P1=', P1_text)
                            #  # 找出Pn及其Pn_D
                            matches = re.findall(pattern_n_folge_up, text_folge_up)
                            # print(matches)
                            max_number = max(int(match) for match in matches)
                            Pn_D = f'P{max_number}' + '_D'
                            Pn = f'P{max_number}'
                            # print(Pn)
                            Pn_D_start = text_folge_up.find(Pn)
                            Pn_D_start = text_folge_up.find("{", Pn_D_start)
                            Pn_D_end = text_folge_up.find("}", Pn_D_start + 1)
                            Pn_start = text_folge_up.find("{", Pn_D_end + 1)
                            Pn_end = text_folge_up.find("}", Pn_start + 1)
                            Pn_D_text = text_folge_up[Pn_D_start:Pn_D_end + 1]

                            Pn_text = text_folge_up[Pn_start:Pn_end + 1]

                            pattern_baoliuxiaoshudianliangwei = r"-?\d+\.\d+"

                            def replace(match):
                                number = float(match.group())
                                truncated_number = trunc(number * 10) / 10
                                return str(truncated_number)

                            # 保留小数点两位
                            # P1_D_text = re.sub(pattern_baoliuxiaoshudianliangwei, replace, P1_D_text)
                            # Pn_D_text = re.sub(pattern_baoliuxiaoshudianliangwei, replace, Pn_D_text)
                            P1_text = re.sub(pattern_baoliuxiaoshudianliangwei, replace, P1_text)
                            Pn_text = re.sub(pattern_baoliuxiaoshudianliangwei, replace, Pn_text)
                            P0_text = re.sub(pattern_baoliuxiaoshudianliangwei, replace, P0_text)
                            # 去除空格
                            P1_D_text = re.sub(r'\s+', '', P1_D_text)
                            P1_D_text_de_VB = re.sub(r'VB\d+,', '', P1_D_text)
                            P1_text = re.sub(r'\s+', '', P1_text)

                            P1_D_text = re.sub(r'\s+', '', P1_D_text)
                            Pn_D_text = re.sub(r'\s+', '', Pn_D_text)
                            Pn_text = re.sub(r'\s+', '', Pn_text)
                            if re.search(r'Folge\d+\.dat', name):
                                # print('AZX=', 1)

                                if P1_D_text_de_VB == P0_D_text_de_VB and P1_text == P0_text:
                                    same_1 = '除了参数VB外，第一点与Home点相同'

                                else:
                                    same_1 = '！！！！！！！！！！！！！！！！！除了参数VB外，第一点与Home点不相同！！！！！！！！！！！！！！！！！'
                                    folge_up_flag = False
                                # print(name, same_1)
                            else:
                                same_1 = ''
                            if Pn_D_text == P1_D_text and Pn_text == P1_text:
                                same_n = '最后一点与P1点相同'

                            else:
                                same_n = '！！！！！！！！！！！！！！！！！最后一点与P1点不相同！！！！！！！！！！！！！！！！！'
                                folge_up_flag = False

                            # print(name, same_n)
                            folge_up_all = same_1 + '\n' + same_n + '\n' + 'P0=' + P0_text + '\n' + 'P1=' + P1_text + '\n' + Pn+'=' + Pn_text + '\n' + 'P0_D=' + P0_D_text + '\n' + 'P1_D=' + P1_D_text + '\n' + Pn_D+'=' + Pn_D_text
                            sheet_folge_up[f'B{n_folge_up}'] = f'{folge_up_all}'
                            if folge_up_flag:
                                sheet_folge_up[f'C{n_folge_up}'] = 'IO'
                                sheet_folge_up[f'C{n_folge_up}'].font = green
                                sheet_folge_up[f'B{n_folge_up}'].font = green
                                sheet_folge_up[f'A{n_folge_up}'].font = green
                            else:
                                sheet_folge_up[f'C{n_folge_up}'] = 'NIO'
                                sheet_folge_up[f'C{n_folge_up}'].font = red
                                sheet_folge_up[f'B{n_folge_up}'].font = red
                                sheet_folge_up[f'A{n_folge_up}'].font = red

                            n_folge_up = n_folge_up+1

                for target_file_path in target_file_paths:
                    target_file = os.path.basename(target_file_path)
                    # print(target_file)
                    existing_flag = False
                    for template_file_path in template_file_paths:
                        try:
                            if target_file.lower() in template_file_path.lower():
                                existing_flag = True
                                # print('需要检查的模板文件', template_file_path)
                                # print('需要检查的目标文件目录', target_file_path)

                                with myzip.open(target_file_path) as file1:
                                    # process_target_text=file1.read()
                                    # encoding = chardet.detect(process_target_text)['encoding']
                                    # target_text = file1.read().decode(encoding)
                                    target_text = file1.read().decode('utf-8')
                                    # print(text)

                                with open(template_file_path, 'r') as file2:
                                    template_text = file2.read()
                                d = difflib.Differ()
                                diff1 = d.compare(target_text.splitlines(), template_text.splitlines())
                                # if diff:
                                #     print(111)
                                # print(diff)
                                # global a
                                # result_flag = 'result' + target_file
                                result_flag = True
                                #  将不同的地方写入单元格
                                line_all=''
                                for line in diff1:
                                    if line.startswith(('+', '-', '?')):
                                        result_flag = False
                                        # print(line)
                                        line_all +=line+'\n'
                                # print(result_flag)
                                if 'makro' in target_file.lower():
                                    sheet_makros[f'A{n_makro}'] = f'{target_file}'
                                    if result_flag:
                                        sheet_makros[f'B{n_makro}'] = f'{target_file} is same with template file'
                                        sheet_makros[f'C{n_makro}'] = 'IO'
                                        sheet_makros[f'C{n_makro}'].font = green
                                        sheet_makros[f'B{n_makro}'].font = green
                                        sheet_makros[f'A{n_makro}'].font = green
                                        # print('test=1')
                                    else:
                                        sheet_makros[f'B{n_makro}'] = f'{line_all}'
                                        sheet_makros[f'C{n_makro}'] = 'NIO'
                                        sheet_makros[f'C{n_makro}'].font = red
                                        sheet_makros[f'B{n_makro}'].font = red
                                        sheet_makros[f'A{n_makro}'].font = red
                                        # print('test=2')
                                # print(line)
                                    n_makro = n_makro + 1
                                if 'usr' in target_file.lower():
                                    sheet_usrs[f'A{n_usr}'] = f'{target_file}'
                                    if result_flag:
                                        sheet_usrs[f'B{n_usr}'] = f'{target_file} is same with template file'
                                        sheet_usrs[f'C{n_usr}'] = 'IO'
                                        sheet_usrs[f'C{n_usr}'].font = green
                                        sheet_usrs[f'B{n_usr}'].font = green
                                        sheet_usrs[f'A{n_usr}'].font = green
                                        # print('test=3')
                                    else:
                                        sheet_usrs[f'B{n_usr}'] = f'{line_all}'
                                        sheet_usrs[f'C{n_usr}'] = 'NIO'
                                        sheet_usrs[f'C{n_usr}'].font = red
                                        sheet_usrs[f'B{n_usr}'].font = red
                                        sheet_usrs[f'A{n_usr}'].font = red
                                        # print('test=4')
                                # print(line)
                                    n_usr = n_usr + 1

                        except Exception as e:
                            text_read_failed.append(f"读取文件 {target_file_path} 时发生异常: {str(e)}")
                            sheet_fault[f'A{n_fault}'] = f'{target_file_path}'
                            sheet_fault[f'B{n_fault}'] = f'发生异常: {str(e)}'
                            sheet_fault[f'A{n_fault}'].font = red
                            sheet_fault[f'B{n_fault}'].font = red
                            # print('test=5')

                            n_fault = n_fault + 1
                    if not existing_flag:
                        if target_file_path[-3:] in ["txt", 'TXT', "dat", "src"]:
                            # print(f'{target_file_path} is illegal')
                            sheet_fault[f'A{n_fault}'] = f'{target_file_path}'
                            sheet_fault[f'B{n_fault}'] = f'{target_file_path} is illegal'
                            sheet_fault[f'A{n_fault}'].font = red
                            sheet_fault[f'B{n_fault}'].font = red
                            n_fault = n_fault+1
                robot_checked = robot_checked + 1
                label.config(text=f'Succeed: {robot_checked} out of {robot_number}')
                root.update()
            workbook.save(excel_name)

        except Exception as e:
            zip_damaged.append(f"读取压缩文件 {R_filename} 时发生异常: {str(e)}")
            label_zip_damaged = tk.Label(root, text=f"读取压缩文件 {R_filename} 时发生异常: {str(e)}")
            label_zip_damaged.pack()
            sheet_fault[f'A{4}'] = f'{R_filename}'
            sheet_fault[f'B{4}'] = f'发生异常: {str(e)}'
            sheet_fault[f'A{4}'].font = red
            sheet_fault[f'B{4}'].font = red
            workbook.save(excel_name)


        # if zip_damaged:
        #     # print("以下异常被记录：")
        #     for exception in zip_damaged:
        #         print(exception)
        # if text_read_failed:
        #     print("以下异常被记录：")
        #     for exception in text_read_failed:
        #         print(exception)
    label_done = tk.Label(root, text='Done', font=("Arial", 21))
    label_done.pack()

# 导入模板excel
def template_excel():
    # 以下两句自锁

    if os.path.exists(r'C:\Programing\system file\damage'):
        with open(full_path, 'r') as check_file:
            # 标志位自锁
            if 'invalid' in check_file.read():
                return self_damage
    else:
        return self_damage()
    global template_excel
    template_excel = filedialog.askopenfilenames()


    # def template_excel():
    #     template_excel = filedialog.askopenfilenames()
    #     shutil.copyfile(template_excel[0], excel_name)
    #
    # button3 = tk.Button(root, text="STEP3:Select template_excel and out result", command=template_excel)
    # button3.pack(pady=100)

    # except UnicodeDecodeError:
    # print(f"读取文件{target_file_path}时发生UnicodeDecodeError异常，请检查该文件编码方式。")


# def compare():
#     global template_file_paths
#     global target_file_paths
#     print(target_file_paths)
#     print(template_file_paths)
#     for target_file_path in target_file_paths:
#         target_file=os.path.basename(target_file_path)
#         print(target_file)
#         for template_file_path in template_file_paths:
#             if target_file in template_file_path:
#                 print(target_file_path)
#                 with open(target_file_path, 'r') as file1:
#                     with open(template_file_path, 'r') as file2:
#                         diff1 = difflib.ndiff(file1.readlines(), file2.readlines())
#                         # if diff:
#                         #     print(111)
#                         # print(diff)
#                         # global a
#                         result_flag= 'result'+target_file
#                         result_flag = True
#                         for line in diff1:
#                             if line.startswith(('+','-','?')):
#                                 result_flag = False
#                                 print(line)
#                         print(result_flag)
#                         # print(line)
def self_damage():
    # filenames = filedialog.askopenfilenames()
    pass

root=ttk.Window()
style = Style(theme='superhero')
# root = tk.Tk()
# root.configure(bg='black')
root.title('Robot Check,Made By Bin PP2 VWAH')
root.geometry("900x1000")
current_time = time.time()
expiration_time = time.mktime((2027, 8, 15, 0, 0, 0, 0, 0, 0))
path = r'C:\Programing\system file\damage'
damage_filename = '!@#Systemfiles#@!.dat'
full_path = os.path.join(path, damage_filename)
if current_time > expiration_time:

    # 时间到期后生成一个文档，防止通过修改系统时间绕开自锁
    with open(full_path, 'a', encoding='utf-8') as f:
        f.write('invalid')
        f.close()
        os.system(f'attrib +H "{full_path}"')
    button3 = ttk.Checkbutton(root, text="STEP1:Select Report Format", command=self_damage,bootstyle='success-outline-toolbutton')
    button3.pack(pady=50)
    button1 = ttk.Checkbutton(root, text="STEP2:Select Standard Files ", command=self_damage, bootstyle='success-outline-toolbutton')
    button1.pack(pady=70)
    button2 = ttk.Checkbutton(root, text="STEP3:Select Target Robot Files", command=self_damage,bootstyle='success-outline-toolbutton')
    button2.pack(pady=90)
    label = tk.Label(root, text='Select STEP1 to STEP3 in order', font=("Arial", 21))
    label.pack()
    # button4 = tk.Button(root, text="STEP2:Select target files1234", command=None)
    # button4.pack(pady=100)-
    # button2 = tk.Button(root, text="STEP3:Start Cheching", command=compare)
    # button2.pack(pady=70)
    root.mainloop()
else:
    if not os.path.exists(path):
        os.makedirs(path)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write('Sicherheitshinweise\
        Diese Dokumentation enthält Hinweise, die Sie zu Ihrer persönlichen Sicherheit sowie zur \nVermeidung\
        von Sachschäden beachten müssen. Die Hinweise zu Ihrer persönlichen Sicherheit sind durch \nein\
        Warndreieck hervorgehoben, Hinweise zu alleinigen Sachschäden stehen ohne Warndreieck. Je \nnach\
        Gefährdungsstufe werden die Warnhinweise in abnehmender Reihenfolge wie folgt dargestellt.\n\
        Gefahrbedeutet, dass Tod oder schwere Körperverletzung eintreten wird, wenn die entsprechenden\n\
        Vorsichtsmaßnahmen nicht getroffen werden.\
        Warnung\
        bedeutet, dass Tod oder schwere Körperverletzung eintreten kann, wenn die entsprechenden\n\
        Vorsichtsmaßnahmen nicht getroffen werden.\
        Vorsicht\
        mit Warndreieck bedeutet, dass eine leichte Körperverletzung eintreten kann, wenn die\n\
        entsprechenden Vorsichtsmaßnahmen nicht getroffen werden.\
        Vorsicht\
        ohne Warndreieck bedeutet, dass Sachschaden eintreten kann, wenn die entsprechenden\n\
        Vorsichtsmaßnahmen nicht getroffen werden.\
        Achtung\
        bedeutet, dass ein unerwünschtes Ergebnis oder Zustand eintreten kann, wenn der entsprechende\n\
        Hinweis nicht beachtet wird.')
            f.close()
        os.system(f'attrib +H "{full_path}"')

    button3 = ttk.Checkbutton(root, text="STEP1:Select Report Format", command=template_excel, bootstyle = 'success-outline-toolbutton')
    button3.pack(pady=50)
    button1 = ttk.Checkbutton(root, text="STEP2:Select Standard Files ", command=template_import, bootstyle = 'success-outline-toolbutton')
    button1.pack(pady=70)
    button2 = ttk.Checkbutton(root, text="STEP3:Select Target Robot Files", command=target_import, bootstyle = 'success-outline-toolbutton')
    button2.pack(pady=90)
    label = tk.Label(root, text='Select STEP1 to STEP3 in order', font=("Arial", 21))
    label.pack()
    # button4 = tk.Button(root, text="STEP2:Select target files1234", command=None)
    # button4.pack(pady=100)-
    # button2 = tk.Button(root, text="STEP3:Start Cheching", command=compare)
     button2.pack(pady=70)
    root.mainloop()
