#!/usr/bin/env python3

from modules.run import Run
import os

if __name__ == '__main__':
    if not os.path.isfile("./lab05_s25_test.py"):
        print("Please place lab05_s25_test.py in this directory")
        exit(1)

    # Run all the tests
    runner = Run("./submissions")
    runner.run("python3 lab07_s25_test.py")
