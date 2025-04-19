#!/usr/bin/env python3

from modules.run import Run
from modules.ilearnzip import ILearnZip
from modules.plagiarism import Plagiarism
import os

if __name__ == '__main__':
    if not os.path.isfile("./test_student_manager.py"):
        print("Please place test_student_manager.py in this directory")
        exit(1)
    if not os.path.isfile("./test_student.py"):
        print("Please place test_student.py in this directory")
        exit(1)

    # Check for plagiarism
    plagiarism_check = Plagiarism(
        "./submissions",
        [
            "test_potion.py",
            ".DS_Store",
            "README.md",
            "README.pdf",
            "ItemsClass.py",
            "Items.py",
            "main.py",
        ],
        [
            r".*.csv",
            r"images/.*",
            r"__pycache__.*",
            r"Data.*",
            r"\.git.*",
            r"\.idea.*"
        ]
    )
    print(plagiarism_check.check_hash_str())
    runner = Run("./submissions")

    i_learn_zip = ILearnZip("", zip_expected=True)
    runner.run("mkdir tests")
    i_learn_zip.inject("./test_student_manager.py", "tests/test_student_manager.py")
    i_learn_zip.inject("./test_student.py", "tests/test_student.py")

    # Run the tests
    runner.run("echo \"Student tests\"; python3 -m unittest discover tests; "
               "echo \"Our tests\"; python3 -m unittest discover .")
