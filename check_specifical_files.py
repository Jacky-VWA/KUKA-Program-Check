# zip_checker.py

import os
import logging
from zipfile import ZipFile

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CheckSpecificalFiles:
    def __init__(self):
        # 在这里输入需要检查的文件名称，确保转换为小写
        self.check_names = [
            "krcdryrun",  # 替换为实际需要检查的文件名
            "kukaloadproject",
            # "specific3"
        ]
        self.check_names = [name.lower() for name in self.check_names]  # 转换为小写

    def extract_zip_file(self, zip_file):
        """提取 ZIP 文件中的所有文件名并返回"""
        try:
            # 检查文件是否存在
            if not os.path.exists(zip_file):
                logging.error(f"文件 {zip_file} 不存在")
                return []

            # 检查文件是否为 ZIP 文件
            if not zip_file.endswith('.zip'):
                logging.error(f"文件 {zip_file} 不是 ZIP 文件")
                return []

            with ZipFile(zip_file, 'r') as z:
                extracted_files = z.namelist()  # 获取 ZIP 文件中的所有文件名
                logging.debug(f"ZIP 文件 {zip_file} 中的所有文件：\n{extracted_files}")

            # 去除路径并转换为小写
            extracted_files = [os.path.basename(file).lower() for file in extracted_files]
            return extracted_files
        except FileNotFoundError as e:
            logging.error(f"文件 {zip_file} 未找到: {e}")
            return []
        except PermissionError as e:
            logging.error(f"没有权限读取文件 {zip_file}: {e}")
            return []
        except BadZipFile as e:
            logging.error(f"文件 {zip_file} 不是有效的 ZIP 文件: {e}")
            return []
        except Exception as e:
            logging.error(f"无法提取 ZIP 文件 {zip_file}: {e}")
            return []

    def run(self, zip_files):
        found_files = set()  # 用于存储已找到的文件名

        # 输出需要检查的文件名
        logging.info(f"需要检查的文件名：{self.check_names}")

        for zip_file in zip_files:
            # 提取 ZIP 文件中的所有文件名
            extracted_files = self.extract_zip_file(zip_file)

            for file in extracted_files:
                file_name = os.path.splitext(file)[0].lower()  # 去除扩展名并转换为小写

                for check_name in self.check_names:
                    if check_name in file_name:
                        logging.info(f"ZIP 文件 {zip_file} 存在文件：{file}")
                        found_files.add(file)  # 记录已找到的文件名

        if not found_files:
            logging.info("没有找到任何匹配的文件。")
            return False, found_files
        else:
            logging.info(f"找到的文件名：{found_files}")
            # 返回值
            return True, found_files