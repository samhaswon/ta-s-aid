from modules.good_job import good_job
from typing import List
import subprocess
import os
import shutil


class UnitTest(object):
    def __init__(self, student_list: List[str], repo_directory: str, test_dir_name="test") -> None:
        """
        Create a UnitTest object to perform unit-testing of student code
        :param student_list: List of student IDs that are used as the name of folders for their repos
        :param repo_directory: directory that the repos are in
        :param test_dir_name: (optional) Name of the test directory in the repo, default of "test"
        """
        self.__repo_directory = repo_directory
        self.__student_list = student_list
        self.__test_dir = test_dir_name

        # Figure out what this system's python command is
        if not os.system("python3 --version"):
            self.__py_cmd = "python3"
        elif not os.system("python --version"):
            self.__py_cmd = "python"
        else:
            self.__py_cmd = "py"
        print(f"Using python command: {self.__py_cmd}")

    def do_tests(self) -> None:
        """
        Run all student tests in a given directory
        :return: None
        """
        results = []
        for student in self.__student_list:
            print(f"Running tests for {student}")
            output = subprocess.Popen(
                f"cd {self.__repo_directory}/{student}/ && {self.__py_cmd} -m unittest discover {self.__test_dir}",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[1].decode("utf-8")
            results.append((student, output))
        for student, output in results:
            # Get the run summary, counting the errors, failures, and passes
            run_result = output.splitlines()[0]
            error_count = run_result.count("E")
            failure_count = run_result.count("F")
            pass_count = run_result.count(".")

            # Add a summary to the output file
            summary = (good_job() + "\n" if not error_count and not failure_count else "") + \
                      f"Errors: {error_count}\n" + \
                      f"Failures: {failure_count}\n" + \
                      f"Passed: {pass_count}\n" + \
                      f"Total: {error_count + failure_count + pass_count}\n" + \
                      "=" * shutil.get_terminal_size((70, 20)).columns + "\n\n"

            # Save the run result
            with open(f"{self.__repo_directory}/{student}.txt", "w") as output_file:
                output_file.write(summary + output)
