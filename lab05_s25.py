#!/usr/bin/env python3

from modules.ilearnzip import ILearnZip
from modules.run import Run
from modules.plagiarism import Plagiarism

if __name__ == '__main__':
    # Check for plagiarism
    plagiarism_check = Plagiarism(
        "./submissions",
        ["test_potion.py", ".DS_Store", "README.md", "README.pdf"],
        [r".*.csv", r"images/.*", r"__pycache__.*", r"Data.*"]
    )
    print(plagiarism_check.check_hash_str())
    # Find the submission .zip file and extract it
    i_learn_zip = ILearnZip("", zip_expected=True)
    i_learn_zip.inject("./lab05_s25_test.py", "lab05_s25_test.py")

    runner = Run("./submissions")
