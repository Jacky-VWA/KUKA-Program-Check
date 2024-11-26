# check_makro_files.py

import os
import logging
from zipfile import ZipFile, BadZipFile  # 导入 BadZipFile 异常

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CheckMakroFiles:
    def __init__(self):
        # 在这里输入需要检查的文件名称，确保转换为小写
        self.check_names = [
            "makro",  # 替换为实际需要检查的文件名
        ]
        self.check_names = [name.lower() for name in self.check_names]  # 转换为小写

    def extract_zip_file(self, zip_file):
        """提取 ZIP 文件中的所有文件名和内容并返回"""
        try:
            # 检查文件是否存在
            if not os.path.exists(zip_file):
                logging.error(f"文件 {zip_file} 不存在")
                return {}

            # 检查文件是否为 ZIP 文件
            if not zip_file.endswith('.zip'):
                logging.error(f"文件 {zip_file} 不是 ZIP 文件")
                return {}

            with ZipFile(zip_file, 'r') as z:
                extracted_files = z.namelist()  # 获取 ZIP 文件中的所有文件名
                logging.debug(f"ZIP 文件 {zip_file} 中的所有文件：\n{extracted_files}")

                # 去除路径并转换为小写
                extracted_files_dict = {}
                for file in extracted_files:
                    file_name = os.path.basename(file).lower()
                    file_content = z.read(file).decode('utf-8', errors='ignore')  # 将内容转换为文本格式
                    extracted_files_dict[file_name] = file_content

            return extracted_files_dict
        except FileNotFoundError as e:
            logging.error(f"文件 {zip_file} 未找到: {e}")
            return {}
        except PermissionError as e:
            logging.error(f"没有权限读取文件 {zip_file}: {e}")
            return {}
        except BadZipFile as e:
            logging.error(f"文件 {zip_file} 不是有效的 ZIP 文件: {e}")
            return {}
        except Exception as e:
            logging.error(f"无法提取 ZIP 文件 {zip_file}: {e}")
            return {}

    def run(self, zip_files, template_file=None):
        found_files = {}  # 用于存储已找到的文件名及其内容
        inconsistent_files = []  # 用于存储与模板不一致的文件名

        # 输出需要检查的文件名
        logging.info(f"需要检查的文件名：{self.check_names}")

        # 如果提供了模板文件，提取模板文件的内容
        template_contents = self.extract_zip_file(template_file) if template_file else {}

        for zip_file in zip_files:
            # 提取 ZIP 文件中的所有文件名和内容
            extracted_files = self.extract_zip_file(zip_file)

            for file_name, file_content in extracted_files.items():
                file_base_name = os.path.splitext(file_name)[0].lower()  # 去除扩展名并转换为小写

                for check_name in self.check_names:
                    if check_name in file_base_name:
                        logging.info(f"ZIP 文件 {zip_file} 存在文件：{file_name}")

                        # 比较文件内容
                        if file_name in template_contents and file_content == template_contents[file_name]:
                            logging.info(f"文件 {file_name} 内容与模板文件一致")
                            found_files[file_name] = file_content
                        else:
                            logging.info(f"文件 {file_name} 内容与模板文件不一致")
                            inconsistent_files.append((os.path.basename(zip_file), file_name))
                        break

        if not found_files:
            logging.info("没有找到任何匹配的文件。")
            return False, found_files, inconsistent_files
        else:
            logging.info(f"找到的文件名：{list(found_files.keys())}")
            return True, found_files, inconsistent_files

# 示例用法
if __name__ == "__main__":
    checker = CheckMakroFiles()
    zip_files = ["path/to/your/zip1.zip", "path/to/your/zip2.zip"]
    template_file = "path/to/your/template.zip"
    result, found_files, inconsistent_files = checker.run(zip_files, template_file)