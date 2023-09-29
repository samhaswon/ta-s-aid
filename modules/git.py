import os
import subprocess
from typing import List, Tuple


class Git(object):
    """
    A simple module to bulk-clone git repos.
    """
    def __init__(self, git_url: str, use_ssh: bool = True):
        self.git_url: str = git_url
        self.ssh: bool = use_ssh

    def clone(self, repo_list: List[Tuple[str, str]], destination: str = "working_dir") -> None:
        commit_summary: List[Tuple[str, str]] = []
        if self.ssh:
            for student, repo in repo_list:
                print(f"Getting {student}'s repo...")
                os.system(f"git clone git@{self.git_url}/{student}/{student}-{repo} {destination}/{student}")
                date = subprocess.Popen(f"cd {destination}/{student}; git log -1 --format=%cd", preexec_fn=os.setsid)
                # os.system(f"cd {destination}/{student}; git log -1 --format=%cd")
                commit_summary += (student, date)

        for student, date in commit_summary:
            print(f"Student: {student}\t\tDate: {date}")
            print("-" * 20)
