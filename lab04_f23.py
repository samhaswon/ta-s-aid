#!/usr/bin/env python3

from modules.ilearnzip import ILearnZip
from modules.import_check import ImportCheck
from modules.unit_test import UnitTest
from modules.plagiarism import Plagiarism
import os

if __name__ == '__main__':
    if not os.path.isfile("./test_potion.py"):
        print("Please place test_potion.py in this directory")
        exit(1)

    # Find the submission .zip file and extract it
    submission_zip: str = [x for x in os.listdir(os.getcwd()) if x.endswith(".zip")][0]
    i_learn_zip = ILearnZip(submission_zip, zip_expected=False)
    i_learn_zip.extract()
    i_learn_zip.inject("./test_potion.py", "test_potion.py")

    # Check for plagiarism
    plagiarism_check = Plagiarism("./submissions", ["test_potion.py"])
    print(plagiarism_check.check_hash_str())

    # Run all the unit tests
    tester = UnitTest("./submissions", "")
    tester.do_tests()

    # Make sure random is imported to follow assignment spec
    import_check = ImportCheck("./submissions")
    import_check.check("potion.py", "random")
