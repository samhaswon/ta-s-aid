from unittest import TestCase
from modules.git import Git
import os


class TestGit(TestCase):
    def test_clone(self):
        try:
            with open("ids.txt", "r") as student_file:
                student_list = student_file.read().splitlines()
            repo_list = [(student, "lab-05-unittest") for student in student_list]
            git = Git("gitlab.csc.tntech.edu:csc2310-sp23-students", True)
            commit_summary = git.clone(repo_list, "test_destination")

            # Get the number of folders and commit summaries, making sure we got everything
            folders = [x[1] for x in os.walk("test_destination")][0]
            self.assertEqual(len(student_list), len(folders))
            self.assertEqual(len(student_list), len(commit_summary))
        except Exception as e:
            self.fail(f"Failure: \n\n{e}")

    def test_git_these(self):
        repo_list = [
            "amykapernick/no_js",
            "github.com:raghur/mermaid-filter.git",
            "/samhaswon/esv_api",
            "git@github.com:brukmula/BasilAppBackEnd.git"
        ]
        git = Git("github.com", debug=True)
        commit_summary = git.these(repo_list, destination="test_destination")

        # Get the number of folders and commit summaries, making sure we got everything
        folders = [x[1] for x in os.walk("test_destination")][0]
        self.assertEqual(len(repo_list), len(folders))
        self.assertEqual(len(repo_list), len(commit_summary))
