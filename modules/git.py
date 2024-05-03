import os
import re
import shutil
import subprocess
from typing import List, Tuple, Union
from modules.helpers.threadwrv import ThreadWRV


class Git(object):
    """
    A simple module to bulk-clone git repos.
    """

    def __init__(self, git_url: str, use_ssh: bool = True, debug: bool = False) -> None:
        """
        :param git_url: base URL for the git repos
        :param use_ssh: True = use ssh to clone the repo
        :param debug: True = print extra debug details
        :returns: None
        """
        self.git_url: str = git_url
        self.ssh: bool = use_ssh
        self.__debug = debug
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

        # Spawn cloning threads for each student
        for student, repo in repo_list:
            print(f"[Git] Getting {student}'s repo...")
            threads.append(ThreadWRV(target=self._clone_thread, args=[clone_type, student, repo, destination]))
            threads[-1].start()

            # Keep the number of cloning threads at or below 4 for gitlab
            if len(threads) >= 4:
                threads[0].join()
                threads.pop(0)

        # Reap the cloning child threads
        for thread in threads:
            thread.join()

        # Spawn new threads to get the last commit date
        threads: List[ThreadWRV] = []
        for student, repo in repo_list:
            threads.append(ThreadWRV(target=self._date_thread, args=[destination, student]))
            threads[-1].start()

        # Reap the date threads and build the summary
        for thread in threads:
            student, date = thread.join()
            commit_summary.append((student, date))

            # Print the summary if requested
            if print_summary:
                print("-" * shutil.get_terminal_size((80, 20)).columns + "\n")
                print(f"[Git] Student: {student}\t\tDate: {date}")
        if print_summary:
            print("=" * shutil.get_terminal_size((80, 20)).columns + "\n")
        return commit_summary

    def these(self,
              repo_list: List[str],
              destination: str = "working_dir",
              print_summary=True) -> \
            List[Tuple[str, str]]:
        """
        Get a list of git repositories.
        :param repo_list: The list of repositories to get. These can be paths, partial URLs, or full clone URLs
        :param destination: The cloning destination for the repository folders
        :param print_summary: (Default True) prints a summary of the commit dates if True
        :return: List of Tuples of the format (username, last commit date)
        """
        # Commit time summary for each student
        commit_summary: List[Union[Tuple[str, str], None]] = []
        # Clone type to use
        clone_type = "git@" if self.ssh else "https://"
        # List of cloning threads
        threads: List[ThreadWRV] = []
        # Username list for commit summary
        username_list: List[str] = []

        # Iterate through the given list and start cloning threads
        for repo in repo_list:
            # Parse the input repo string
            if clone_type in repo:
                # Repo string is fully built
                url = repo
            elif self.git_url in repo:
                # Git URL just needs to be prepended
                url = clone_type + repo
            else:
                # We just have the path, so we need to build everything based on the clone type
                if repo[0] == "/" and self.ssh:
                    url = clone_type + self.git_url + ":" + repo[1:]
                elif repo[0].isalnum() and self.ssh:
                    url = clone_type + self.git_url + ":" + repo
                elif repo[0].isalnum():
                    url = clone_type + self.git_url + "/" + repo[1:]
                else:
                    url = clone_type + self.git_url + repo

            # Extract username using regular expression
            match = re.search(r'[:/](\w+)/', url)
            if match:
                # The first match should be the username
                username = match.group(1)
                if self.__debug:
                    print(f"[Git] Username: {username}")
            # If URL parsing fails, skip it
            else:
                print(f"[Git] Invalid repo: {repo}")
                continue
            # Print the built URL for debugging
            if self.__debug:
                print(f"[Git] Built URL: {url}")
            print(f"[Git] Getting {username}'s repo")

            # Spawn and start the cloning thread
            threads.append(ThreadWRV(target=self._clone_this, args=[url, username, destination]))
            threads[-1].start()

            # Keep the running threads at or below 4
            if len(threads) >= 4:
                threads[0].join()
                threads.pop(0)

            # Add the username to the list for later
            username_list.append(username)

        # Reap clone child threads
        for thread in threads:
            thread.join()

        # Spawn more threads for getting the date summary
        threads: List[ThreadWRV] = []
        for username in username_list:
            threads.append(ThreadWRV(target=self._date_thread, args=[destination, username]))
            threads[-1].start()

        # Reap date child threads
        for thread in threads:
            student, date = thread.join()
            commit_summary.append((student, date))

            # Print the date summary if desired
            if print_summary:
                print("-" * shutil.get_terminal_size((80, 20)).columns + "\n")
                print(f"[Git] Student: {student}\t\tDate: {date}")
        if print_summary:
            print("=" * shutil.get_terminal_size((80, 20)).columns + "\n")
        return commit_summary

    def _clone_thread(self, clone_type, student, repo, destination, depth: int = 0) -> None:
        # Clone the repo
        if os.system(f"git clone {clone_type}{self.git_url}/{student}/{student}-{repo} {destination}/{student}") and \
                depth < 4:
            if self.__debug:
                print(f"[Git] Clone failure for {student}; count: {depth + 1}")
            # Recurse on failure
            self._clone_thread(clone_type, student, repo, destination, depth + 1)
        # Base condition if the cloning keeps failing for whatever reason
        elif depth >= 4:
            print(f"[Git] failure count exceeded for {student}'s repo")

    def _clone_this(self, repo_url: str, username: str, destination: str, depth: int = 0) -> None:
        # Clone the repo
        if os.system(f"git clone {repo_url} {destination}/{username}") and \
                depth < 4:
            if self.__debug:
                print(f"[Git] Clone failure for {username}; count: {depth + 1}")
            # Recurse on failure
            self._clone_this(repo_url, username, destination, depth + 1)
        # Base condition if the cloning keeps failing for whatever reason
        elif depth >= 4:
            print(f"[Git] failure count exceeded for {username}'s repo")

    @staticmethod
    def _date_thread(destination: str, student: str) -> Tuple[str, str]:
        # Use git log to get the last commit date
        return student, subprocess.Popen(f"cd {destination}/{student} && git log -1 --format=%cd",
                                         stdout=subprocess.PIPE, shell=True).communicate()[0].decode("utf-8")
