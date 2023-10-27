from modules.good_job import good_job
from typing import List
import subprocess
import os
import shutil


class UnitTest(object):
    def __init__(self, student_list: List[str], repo_directory: str, test_dir_name="test"):
        self.__repo_directory = repo_directory
        self.__student_list = student_list
        self.__test_dir = test_dir_name

        if not os.system("python3 --version"):
            self.__py_cmd = "python3"
        elif not os.system("python --version"):
            self.__py_cmd = "python"
        else:
            self.__py_cmd = "py"

    def do_tests(self):
        results = []
        for student in self.__student_list:
            print(f"Running tests for {student}")
            output = subprocess.Popen(
                f"cd {self.__repo_directory}/{student}/ && {self.__py_cmd} -m unittest discover {self.__test_dir}",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[1].decode("utf-8")
            results.append((student, output))
        for student, output in results:
            run_result = output.splitlines()[0]
            error_count = run_result.count("E")
            failure_count = run_result.count("F")
            pass_count = run_result.count(".")
            summary = good_job() \
                if not error_count \
                and not failure_count \
                else "" + \
                     f"Errors: {error_count}\n" + \
                     f"Failures: {failure_count}\n" + \
                     f"Passed: {pass_count}\n" + \
                     f"Total: {error_count + failure_count + pass_count}\n" + \
                     "=" * shutil.get_terminal_size((80, 20)).columns + "\n\n"
            with open(f"{self.__repo_directory}/{student}.txt", "w") as output_file:
                output_file.write(summary + output)
