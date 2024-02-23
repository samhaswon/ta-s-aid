from modules.ilearnzip import ILearnZip
import os
from modules.plagiarism import Plagiarism

if __name__ == '__main__':
    submission_zips: list = [x for x in os.listdir(os.getcwd()) if x.endswith(".zip")]

    print("Select a file from the following by index:")
    for i in range(1, len(submission_zips) + 1):
        print(f"{i} {submission_zips[i - 1]}")

    try:
        selection = int(input("\n> "))
    except ValueError:
        print("Invalid selection type")
        exit(1)

    if selection > len(submission_zips):
        print("Invalid selection")
        exit(1)

    i_learn_zip = ILearnZip(submission_zips[selection - 1], zip_expected=True)
    i_learn_zip.extract()

    plagiarism_check = Plagiarism("./submissions",
                                  ["contacts.json", "events.json",
                                   ],
                                  [r"env", r"idea", r"MACOSX", r"git", r"pdf$", r"events.json", r"contacts.json",
                                   r"pycache", r"tests", r"UI", r"main\.py", r"README\.md", r"Calendar", r"Contact",
                                   r"Event\.py", r".*init__\.py"
                                   ])
    print(plagiarism_check.check_hash_str())
