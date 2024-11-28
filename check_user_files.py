import zipfile
import os

class CheckUserFiles:
    def run(self, zip_files, template_file=None):
        """
        检查用户文件的逻辑。

        参数:
            zip_files (list): ZIP 文件路径列表。
            template_file (str): 模板文件路径（可选）。

        返回:
            tuple: 检查结果和找到的差异文件。
        """
        found_files_zip = {}
        found_files_template = {}
        differences = []

        # 检查 ZIP 文件中的 src 文件
        self.extract_src_files(zip_files, found_files_zip)

        # 检查模板文件中的 src 文件
        if template_file:
            self.extract_src_files([template_file], found_files_template)

        # 对比 ZIP 文件和模板文件中的相同文件
        differences = self.compare_files(found_files_zip, found_files_template)

        result = len(differences) == 0  # 如果没有差异，则结果为 True
        return result, differences

    def extract_src_files(self, zip_files, found_files):
        """从 ZIP 文件中提取 .src 文件并保存为文本文件。"""
        for zip_file in zip_files:
            with zipfile.ZipFile(zip_file, 'r') as z:
                for file_info in z.infolist():
                    if file_info.filename.lower().endswith('.src') and ('user_s' in file_info.filename.lower() or 'user_r' in file_info.filename.lower()):
                        # 提取并转换为文本文件
                        with z.open(file_info.filename) as src_file:
                            content = src_file.read().decode('utf-8')
                            text_file_name = f"{file_info.filename}.txt"
                            with open(text_file_name, 'w') as text_file:
                                text_file.write(content)
                            found_files[file_info.filename] = text_file_name

    def compare_files(self, found_files_zip, found_files_template):
        """比较 ZIP 文件和模板中的相同文件，返回差异文件列表。"""
        differences = []
        for filename, zip_text_file in found_files_zip.items():
            template_text_file = found_files_template.get(filename)
            if template_text_file:
                # 比较文件内容
                with open(zip_text_file, 'r') as zip_file:
                    zip_content = zip_file.read()
                with open(template_text_file, 'r') as template_file:
                    template_content = template_file.read()

                if zip_content != template_content:
                    differences.append(filename)

        return differences
