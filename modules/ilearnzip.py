from datetime import datetime
import os
from pathlib import Path
import re
import shutil
from typing import Union
from zipfile import BadZipfile, ZipFile as BrokenZipFile


class ZipFile(BrokenZipFile):
    """
    Corrects a bug present in the standard library and makes this class more appropriate for this application.
    """

    def __init__(self, *args, **kwargs):
        """
        Pass everything to the standard lib ZipFile
        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(*args, **kwargs)

    @classmethod
    def _sanitize_windows_name(cls, arcname, pathsep):
        """Fix the standard lib's sanitization"""
        return re.sub(r"(?<=[/\w\\]) (?=[/\\])|(?<=[/\w\\]) $", "",
                      super()._sanitize_windows_name(arcname, pathsep))  # PyCharm hates this, but it works

    def extractall(self, path=None, members=None, pwd=None):
        """
        Fix for the security hole of zip bombs by reimplementing extractall and ignoring those files. Also ignores
        __pycache__/ and .idea/ folders
        """
        if members is None:
            members = self.namelist()

        path = os.getcwd() if path is None else os.fspath(path)

        for zipinfo in members:
            if "__MACOSX/" in zipinfo or ".DS_Store" in zipinfo or ".idea" in zipinfo or "__pycache__" in zipinfo:
                continue
            self._extract_member(zipinfo, path, pwd)


class ILearnZip(object):
    def __init__(self, path_to_zip: str, output_dir: str = "submissions", zip_expected: bool = True):
        self.__path_to_zip = path_to_zip
        self.__output_dir = output_dir
        self.__zip_expected = zip_expected

    def extract(self, normalize_filename: Union[str, None] = None) -> None:
        """
        Extract the given zip file
        :param normalize_filename: Name to normalize files to if provided
        :return: None
        """
        # Extract the main zip file
        if os.path.isdir(self.__output_dir):
            delete_existing = input(f"{self.__output_dir} already exists. Removing it will allow extraction to "
                                    f"continue. Would you like to remove it? (y/n) ")
            if delete_existing.lower() == "y":
                shutil.rmtree(self.__output_dir)
            else:
                return
        try:
            with ZipFile(self.__path_to_zip, "r") as sub_zip:
                sub_zip.testzip()
                sub_zip.extractall(path=self.__output_dir)
        except BadZipfile as e:
            print(f"[Zip] Bad iLearn Zip File:\n\n{e}")
            exit(1)
        # Remove the annoying index.html file
        os.remove(f"{self.__output_dir + os.path.sep}index.html")

        # Keep only the most recent submission
        directory_name = os.getcwd() + os.path.sep + self.__output_dir
        sub_list = [x[2] for x in os.walk(directory_name)][0]
        for submission in sub_list:
            i_learn_id = submission[:15]
            student_sub_list = list(filter(lambda x: i_learn_id in x, sub_list))
            if len(student_sub_list) > 1:
                max_date = None
                latest_submission = None
                latest_list = []

                # Find the latest submission
                for sub in student_sub_list:
                    date_match = re.search(r'([A-Za-z]{3} \d{1,2}, \d{4} \d{1,4} [AP]M)', sub)

                    if date_match:
                        date_str = date_match.group()
                        date = datetime.strptime(date_str, '%b %d, %Y %I%M %p')

                        if max_date is None or date > max_date:
                            max_date = date
                            latest_submission = sub
                            latest_list = [sub]
                        elif date == max_date:
                            latest_list.append(sub)
                # Remove the student's other submissions
                for sub in sub_list:
                    if i_learn_id in sub and sub not in latest_list:
                        os.remove(directory_name + os.path.sep + sub)
                        sub_list.remove(sub)

        # Get a list of all the submitted files
        sub_list = [x[2] for x in os.walk(directory_name)][0]

        # Extract the sub zip files
        for submission in sub_list:
            if submission.endswith(".zip"):
                if not self.__zip_expected:
                    print(f"[Zip] Zip submission: {submission}")
                try:
                    unzip_it = True
                    # Adapted from: https://rules.sonarsource.com/python/RSPEC-5042/
                    threshold_entries = 10000
                    threshold_size = 1000000000
                    threshold_ratio = 20

                    total_size_archive = 0
                    total_entry_archive = 0
                    zfile = ZipFile(f"{self.__output_dir}/{submission}")
                    zfile.testzip()
                    for zinfo in zfile.infolist():
                        data = zfile.read(zinfo)

                        total_entry_archive += 1

                        total_size_archive += len(data)
                        if zinfo.compress_size:
                            ratio = len(data) / zinfo.compress_size
                        else:
                            ratio = 0

                        if ratio > threshold_ratio:
                            # Macs are weird in their creation of zip files, so account for that.
                            if (zinfo.filename.startswith("__MACOSX/") or ".DS_Store" in zinfo.filename) and ratio < 98:
                                continue
                            print(f"![Zip] ERROR: Highly compressed zip file. Could be a zip bomb. {submission}")
                            unzip_it = False
                            break
                        if total_size_archive > threshold_size:
                            print(f"![Zip] ERROR: Weirdly large zip file. Not decompressing. {submission}")
                            unzip_it = False
                            break
                        if total_entry_archive > threshold_entries:
                            print(f"![Zip] ERROR: Too many files. Not decompressing. {submission}")
                            unzip_it = False
                            break
                    if unzip_it:
                        start = submission.find("-", 9) + 2
                        end = submission.find("- ", start)
                        path = self.__output_dir + os.path.sep + submission[start:end]
                        zfile.extractall(path=path)
                    zfile.close()
                    os.remove(self.__output_dir + os.path.sep + submission)
                except BadZipfile as e:
                    print(f"![Zip] ERROR: Bad zip file submission: {submission}; {e}")
            elif self.__zip_expected:
                print(f"[Zip] Received non-zip submission: {submission}")

        # Get all the students' names
        sub_list = [x[2] for x in os.walk(directory_name)][0]
        student_list = [x[x.find("-", 9) + 2:x.rfind("-",
                                                     0, x.rfind("-") if x.count("-") == 4 else
                                                     x.rfind("-", 0, x.rfind("-")))].strip()
                        for x in sub_list]

        # Make their folders, moving their submission into their folder
        for student in student_list:
            # Don't make the folder if it exists
            if not Path.is_dir(Path(directory_name + os.path.sep + student).absolute()):
                os.mkdir(directory_name + os.path.sep + student)

            # Find their files in the submissions
            student_files = list(filter(lambda x: re.search(r"\s" + student, x), sub_list))

            for file in student_files:
                base_name = re.search(r"(?<=[A|P]M\s-\s).+", file).group(0)
                if normalize_filename and base_name != normalize_filename:
                    print(f"[iLearn] Normalizing {base_name} to {normalize_filename} for {student}")
                    base_name = normalize_filename
                # Put their files in their folder
                src_file = os.path.join(directory_name, file)
                dest_file = os.path.join(directory_name, student, base_name)
                if not os.path.isfile(dest_file):
                    os.rename(src_file, dest_file)

    def inject(self, file: str, output: Union[str, None]) -> None:
        """
        Inject the given file into the student's submission directory
        :param file: Relative path to the file to inject
        :param output: (optional) name in the student directory to inject the file as
        :return: None
        """
        if not output:
            output = file
        if output.startswith("./"):
            output = output[2:]
        student_list = [x[1] for x in os.walk(os.getcwd() + os.path.sep + self.__output_dir)][0]
        for student in student_list:
            shutil.copy(file, self.__output_dir + os.path.sep + student + os.path.sep + output)
