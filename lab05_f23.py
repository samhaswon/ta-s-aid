#!/usr/bin/env python3

from modules.ilearnzip import ILearnZip
from modules.unit_test import UnitTest
from modules.plagiarism import Plagiarism
import os

if __name__ == '__main__':
    if not os.path.isfile("./test_sandwich.py"):
        print("Please place test_sandwich.py in this directory")
        exit(1)

    # Find the submission .zip file and extract it
    submission_zip: str = [x for x in os.listdir(os.getcwd()) if x.endswith(".zip") and "Lab 5" in x][0]
    i_learn_zip = ILearnZip(submission_zip, zip_expected=False)
    i_learn_zip.extract(normalize_filename="sandwich.py")
    i_learn_zip.flatten()

    # Check for plagiarism
    plagiarism_check = Plagiarism("./submissions", [])
    print(plagiarism_check.check_hash_str())

    # Inject the test
    i_learn_zip.inject("./test_sandwich.py", "test_sandwich.py")

    # Run all the unit tests
    tester = UnitTest("./submissions", "")
    tester.do_tests()
