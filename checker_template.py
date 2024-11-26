# checker_template.py

from check_specifical_files import CheckSpecificalFiles
# from check_folge_files import CheckFolgeFiles
# from check_up_files import CheckUpFiles
# from check_makro_files import CheckMakroFiles
# from check_user_files import CheckUserFiles
# from check_hardware_files import CheckHardwareFiles

class CheckerTemplate:
    def __init__(self, files, template_file):
        self.files = files
        self.template_file = template_file  # 新增模板文件属性
        self.checks = [
            CheckSpecificalFiles(),
            # CheckFolgeFiles(),
            # CheckUpFiles(),
            # CheckMakroFiles(),
            # CheckUserFiles(),
            # CheckHardwareFiles(),
        ]
        self.results = []

    def run_checks(self, files=None):
        """执行所有检查并生成报告"""
        # 如果传入了files参数，覆盖当前实例的self.files
        if files is not None:
            self.files = files

        try:
            for check in self.checks:
                # 运行checks里的run，并将返回值给到check_results
                check_results = check.run(self.files)
                self.results.extend(check_results)

            self.generate_report()  # 生成报告

            return self.results  # 返回检查结果
        except Exception as e:
            print(f"检查过程中发生错误: {e}")
            return []  # 返回空列表以表示出错


