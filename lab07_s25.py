#!/usr/bin/env python3

from modules.run import Run
from modules.ilearnzip import ILearnZip
import os

if __name__ == '__main__':
    if not os.path.isfile("./lab05_s25_test.py"):
        print("Please place lab05_s25_test.py in this directory")
        exit(1)

    i_learn_zip = ILearnZip("", zip_expected=True)
    i_learn_zip.inject("./lab07_s25_test.py", "lab07_s25_test.py")

    # Run all the tests
    runner = Run("./submissions")

    # Fix the branch stuff from cloning
    runner.run("git config remote.origin.fetch \"+refs/heads/*:refs/remotes/origin/*\"")
    runner.run("git fetch origin")
    runner.run(
        "for b in $(git branch -r | "
        "grep '^  origin/' | "
        "grep -vE 'HEAD|main' | "
        "sed 's|  origin/||'); do "
        "git branch --track \"$b\" \"origin/$b\" 2>/dev/null; "
        "done"
    )
    runner.run("python3 lab07_s25_test.py")
