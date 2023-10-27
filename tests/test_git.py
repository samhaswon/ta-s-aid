from unittest import TestCase
from modules.git import Git


class TestGit(TestCase):
    def test_clone(self):
        try:
            with open("ids.txt", "r") as student_file:
                student_list = student_file.read().splitlines()
            repo_list = [(student, "lab-05-unittest") for student in student_list]
            git = Git("gitlab.csc.tntech.edu:csc2310-sp23-students", True)
            git.clone(repo_list, "test_destination")
        except Exception as e:
            self.fail(f"Failure: \n\n{e}")
