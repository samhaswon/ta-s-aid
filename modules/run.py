import os
import subprocess
from modules.helpers.threadwrv import ThreadWRV
from typing import List, Tuple


class Run(object):
    """
    Run commands in a student's folder
    """
    def __init__(self, directory):
        """
        Set up a run object for running commands in student folders
        :param directory: Directory where the student folders are
        """
        self.__directory = directory
        self.__student_list: List[str] = [x[1] for x in os.walk(directory)][0]

    def run(self, command: str) -> None:
        """
        Runs the specified command in students' folders
        :param command: The command to run
        :return: None
        """
        results = []
        threads = []
        for student in self.__student_list:
            threads.append(ThreadWRV(target=self._run_thread, args=[command, student]))
            threads[-1].start()
        for thread in threads:
            results.append(thread.join())
        for result in results:
            self._save_result(*result)

    def _run_thread(self, command: str, sub_folder: str) -> Tuple[str, str]:
        """
        Runs the specified command in the specified sub_folder
        :param command: the command to run
        :param sub_folder: folder to run the command in
        :return: folder name, output string
        """
        process = subprocess.Popen(
            f"cd {self.__directory}/{sub_folder}/ && {command}",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        try:
            output = process.communicate(timeout=10)
            return sub_folder, output[1].decode("utf-8") + output[0].decode("utf-8")
        except subprocess.TimeoutExpired:
            print(f"![Run] Test thread timeout expired for {sub_folder}")
            process.kill()
            return sub_folder, "Timeout expired"

    def _save_result(self, student: str, result: str) -> None:
        """
        Saves the given string to a file for the given student.
        :param student: Student name for the basename of the text file.
        :param result: The string to write to the student's file
        :return: None
        """
        with open(f"{self.__directory}/{student}.txt", "w") as output_file:
            output_file.write(result)
