import os
import shutil
import subprocess
from typing import List, Tuple


class Git(object):
    """
    A simple module to bulk-clone git repos.
    """
    def __init__(self, git_url: str, use_ssh: bool = True) -> None:
        """
        :param git_url: base URL for the git repos
        :param use_ssh: True = use ssh to clone repos
        :returns: None
        """
        self.git_url: str = git_url
        self.ssh: bool = use_ssh

    def clone(self, repo_list: List[Tuple[str, str]], destination: str = "working_dir") -> List[Tuple[str, str]]:
        """
        Clone the student's repos to a working directory
        :param repo_list: List of student names and repo (format) additions that make the name of the repo
        :param destination: Place for the cloned repos to go
        :return: List of Tuples of the format (student, last commit date)
        """
        commit_summary: List[Tuple[str, str]] = []
        if self.ssh:
            for student, repo in repo_list:
                print(f"Getting {student}'s repo...")
                os.system(f"git clone git@{self.git_url}/{student}/{student}-{repo} {destination}/{student}")
                date = subprocess.Popen(f"cd {destination}/{student} && git log -1 --format=%cd",
                                        stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")
                commit_summary.append((student, date))
        else:
            for student, repo in repo_list:
                print(f"Getting {student}'s repo...")
                os.system(f"git clone https://{self.git_url}/{student}/{student}-{repo} {destination}/{student}.git")
                date = subprocess.Popen(f"cd {destination}/{student} && git log -1 --format=%cd",
                                        stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")
                commit_summary += (student, date)

        for student, date in commit_summary:
            print("-" * shutil.get_terminal_size((80, 20)).columns + "\n")
            print(f"Student: {student}\t\tDate: {date}")
        print("-" * shutil.get_terminal_size((80, 20)).columns + "\n")
        return commit_summary
