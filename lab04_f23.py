#!/usr/bin/env python3

from datetime import datetime
from modules.unit_test import UnitTest
import os
from pathlib import Path
import re
import shutil
from zipfile import ZipFile

if __name__ == '__main__':
    if not os.path.isfile("./test_potion.py"):
        print("Please place test_potion.py in this directory")
        exit(1)
    # Find the submission .zip file and extract it
    submission_zip: str = [x for x in os.listdir(os.getcwd()) if x.endswith(".zip")][0]

    with ZipFile(submission_zip, "r") as sub_zip:
        sub_zip.extractall(path="./submissions")

    os.remove("./submissions/index.html")

    # Get a list of all the submitted files
    directory_name = os.getcwd() + os.path.sep + "submissions"
    sub_list = [x[2] for x in os.walk(directory_name)][0]

    for submission in sub_list:
        if submission.endswith(".zip"):
            print(f"Zip submission: {submission}")
            unzip_it = True
            # Adapted from: https://rules.sonarsource.com/python/RSPEC-5042/
            THRESHOLD_ENTRIES = 10000
            THRESHOLD_SIZE = 1000000000
            THRESHOLD_RATIO = 10

            totalSizeArchive = 0
            totalEntryArchive = 0
            zfile = ZipFile(f"./submissions/{submission}")
            for zinfo in zfile.infolist():
                data = zfile.read(zinfo)

                totalEntryArchive += 1

                totalSizeArchive += len(data)
                ratio = len(data) / zinfo.compress_size

                if ratio > THRESHOLD_RATIO:
                    print("Highly compressed zip file. Could be a zip bomb.")
                    unzip_it = False
                    break
                if totalSizeArchive > THRESHOLD_SIZE:
                    print("Weirdly large zip file. Not decompressing")
                    unzip_it = False
                    break
                if totalEntryArchive > THRESHOLD_ENTRIES:
                    print("Too many files. Not decompressing.")
                    unzip_it = False
                    break
            if unzip_it:
                zfile.extractall(path="./submissions")
            zfile.close()
            os.remove(f"./submissions/{submission}")

    # Get the submission list again after extraction
    sub_list = [x[2] for x in os.walk(directory_name)][0]

    # Check for multiple submissions, removing all but the latest one
    for submission in sub_list:
        iLearn_id = submission[:15]
        student_sub_list = list(filter(lambda x: iLearn_id in x, sub_list))
        if len(student_sub_list) > 1:
            max_date = None
            latest_submission = None

            # Find the latest submission
            for sub in student_sub_list:
                date_match = re.search(r'([A-Za-z]{3} \d{1,2}, \d{4} \d{1,4} [AP]M)', sub)

                if date_match:
                    date_str = date_match.group()
                    date = datetime.strptime(date_str, '%b %d, %Y %I%M %p')

                    if max_date is None or date > max_date:
                        max_date = date
                        latest_submission = sub
            # Remove the student's other submissions
            for sub in sub_list:
                if iLearn_id in sub and sub != latest_submission:
                    os.remove(f"./submissions/{sub}")
                    sub_list.remove(sub)

    # Get all the students' names
    student_list = [x[18:x.find("-", 18)] for x in sub_list]

    # Make their folders, moving their submission into their folder along with the unit test
    for student in student_list:
        # Don't make the folder if it exists
        if not Path.is_dir(Path(directory_name + os.path.sep + student).absolute()):
            os.mkdir(directory_name + os.path.sep + student)

        # Find their file in the submissions
        student_file = list(filter(lambda x: student in x, sub_list))[0]

        # Put their file in their folder
        src_file = os.path.join(directory_name, student_file)
        dest_file = os.path.join(directory_name, student, "potion.py")
        if not os.path.isfile(dest_file):
            os.rename(src_file, dest_file)

        # Put the test in their folder
        shutil.copy("./test_potion.py", f"./submissions/{student}/test_potion.py")

    # Run all the unit tests
    tester = UnitTest(student_list, directory_name, "")
    tester.do_tests()
