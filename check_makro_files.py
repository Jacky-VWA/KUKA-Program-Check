import os
import logging
from zipfile import ZipFile, BadZipFile  # 导入 BadZipFile 异常

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CheckMakroFiles:
    def __init__(self):
        # 需要检查的文件名称，确保转换为小写
        self.check_names = ["makro"]
        self.check_extension = ".src"  # 只查找 .src 文件
        self.check_names = [name.lower() for name in self.check_names]  # 转换为小写

    def extract_zip_file(self, zip_file):
        """提取 ZIP 文件中的所有文件名和内容并返回"""
        try:
            if not os.path.exists(zip_file):
                logging.error(f"文件 {zip_file} 不存在")
                return {}

            if not zip_file.endswith('.zip'):
                logging.error(f"文件 {zip_file} 不是 ZIP 文件")
                return {}

            with ZipFile(zip_file, 'r') as z:
                extracted_files = z.namelist()
                if not extracted_files:
                    logging.warning(f"ZIP 文件 {zip_file} 是空的。")
                    return {}

                logging.debug(f"ZIP 文件 {zip_file} 中的所有文件：\n{extracted_files}")

                extracted_files_dict = {}
                for file in extracted_files:
                    file_name = os.path.basename(file).lower()
                    file_content = z.read(file).decode('utf-8', errors='ignore')
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
        found_files = {}
        inconsistent_files = []

        logging.info(f"需要检查的文件名：{self.check_names}，扩展名：{self.check_extension}")

        # 提取模板文件内容
        template_contents = self.extract_zip_file(template_file) if template_file else {}

        for zip_file in zip_files:
            extracted_files = self.extract_zip_file(zip_file)

            for file_name, file_content in extracted_files.items():
                file_base_name = os.path.splitext(file_name)[0].lower()

                # 只检查包含 "makro" 且扩展名为 .src 的文件
                if any(check_name in file_base_name for check_name in self.check_names) and file_name.endswith(self.check_extension):
                    logging.info(f"ZIP 文件 {zip_file} 存在文件：{file_name}")

                    if file_name in template_contents:
                        if file_content != template_contents[file_name]:  # 检查不一致
                            logging.info(f"文件 {file_name} 内容与模板文件不一致")
                            inconsistent_files.append((os.path.basename(zip_file), file_name, file_content[:50]))  # 记录前50个字符
                    else:
                        logging.warning(f"文件 {file_name} 在模板文件中未找到。")

        if not inconsistent_files:
            logging.info("没有找到任何与模板不一致的文件。")
            return False, found_files, inconsistent_files
        else:
            logging.info(f"找到的不一致文件名：{list(set([file[1] for file in inconsistent_files]))}")
            return True, found_files, inconsistent_files
