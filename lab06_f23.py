#!/usr/bin/env python3

from modules.ilearnzip import ILearnZip
from modules.run import Run
from modules.plagiarism import Plagiarism
import os

if __name__ == '__main__':
    if not os.path.isfile("./lab06f23_test.py"):
        print("Please place lab06f23_test.py in this directory")
        exit(1)
    if not os.path.isfile("./students.json"):
        print("Please place students.json in this directory")
        exit(1)

    # Find the submission .zip file and extract it
    submission_zip: str = [x for x in os.listdir(os.getcwd()) if x.endswith(".zip") and "Lab 06" in x][0]
    i_learn_zip = ILearnZip(submission_zip, zip_expected=False)
    i_learn_zip.extract(normalize_filename="student.py")

    # Check for plagiarism
    plagiarism_check = Plagiarism("./submissions")
    print(plagiarism_check.check_hash_str())

    # Inject the test
    i_learn_zip.inject("./lab06f23_test.py", "lab06f23_test.py")
    i_learn_zip.inject("./students.json", "students.json")

    # Run all the unit tests
    tester = Run("./submissions")
    tester.run("py lab06f23_test.py")
