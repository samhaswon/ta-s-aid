from modules.ilearnzip import ILearnZip
from modules.unit_test import UnitTest
from modules.plagiarism import Plagiarism
import os

if __name__ == '__main__':
    if not os.path.isfile("examples/it1_s24.py"):
        print("Please place test_it1.py in this directory")
        exit(1)

    # Find the submission .zip file and extract it
    submission_zip: str = \
        [x for x in os.listdir(os.getcwd()) if x.endswith(".zip") and "Term Project - Iteration 1" in x][0]
    i_learn_zip = ILearnZip(submission_zip, zip_expected=True)
    i_learn_zip.extract()
    i_learn_zip.flatten()

    # Check for plagiarism
    plagiarism_check = Plagiarism("./submissions",
                                  [],
                                  [
                                      r"env", r"idea", r"MACOSX", r"git", r"pdf$", r"events\.json", r"contacts\.json",
                                      r"pycache", r"tests", r"UI", r"main\.py", r"README\.md", r"Calendar",
                                      r".init__\.py", r".exe$"
                                  ])
    print(plagiarism_check.check_hash_str())

    # Inject the test
    i_learn_zip.inject("examples/it1_s24.py", "test_it1.py")

    # Run all the unit tests
    tester = UnitTest("./submissions", "")
    tester.do_tests()
