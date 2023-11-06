import os
import shutil
import subprocess
from typing import List, Tuple, Union
from modules.helpers.threadwrv import ThreadWRV


class Git(object):
    """
    A simple module to bulk-clone git repos.
    """

    def __init__(self, git_url: str, use_ssh: bool = True) -> None:
        """
        :param git_url: base URL for the git repos
        :param use_ssh: True = use ssh to clone the repo
        :returns: None
        """
        self.git_url: str = git_url
        self.ssh: bool = use_ssh
        if os.system("git --version"):
            print("Git is not installed. Exiting...")
            exit(1)

    def clone(self,
              repo_list: List[Tuple[str, str]],
              destination: str = "working_dir",
              print_summary=True) -> \
            List[Tuple[str, str]]:
        """
        Clone the student's repos to a working directory
        :param repo_list: List of student names and repo (format) additions that make the name of the repo
        :param destination: Place for the cloned repos to go
        :param print_summary: (Default True) prints a summary of the commit dates if True
        :return: List of Tuples of the format (student, last commit date)
        """
        commit_summary: List[Union[Tuple[str, str], None]] = []
        clone_type = "git@" if self.ssh else "https://"
        threads: List[ThreadWRV] = []
        for student, repo in repo_list:
            print(f"[Git] Getting {student}'s repo...")
            threads.append(ThreadWRV(target=self._clone_thread, args=[clone_type, student, repo, destination]))
            threads[-1].start()
            if len(threads) >= 4:
                threads[0].join()
                threads.pop(0)
        for thread in threads:
            thread.join()
        threads: List[ThreadWRV] = []
        for student, repo in repo_list:
            threads.append(ThreadWRV(target=self._date_thread, args=[destination, student]))
            threads[-1].start()

        for thread in threads:
            student, date = thread.join()
            commit_summary.append((student, date))

            if print_summary:
                print("-" * shutil.get_terminal_size((80, 20)).columns + "\n")
                print(f"[Git] Student: {student}\t\tDate: {date}")
        print("=" * shutil.get_terminal_size((80, 20)).columns + "\n")
        return commit_summary

    def _clone_thread(self, clone_type, student, repo, destination, depth=0) -> None:
        if os.system(f"git clone {clone_type}{self.git_url}/{student}/{student}-{repo} {destination}/{student}") and \
                depth < 4:
            self._clone_thread(clone_type, student, repo, destination, depth + 1)
        elif depth >= 4:
            print(f"[Git] failure count exceeded for {student}'s repo")

    @staticmethod
    def _date_thread(destination: str, student: str) -> Tuple[str, str]:
        return student, subprocess.Popen(f"cd {destination}/{student} && git log -1 --format=%cd",
                                         stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")
