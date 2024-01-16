import hashlib
import os
import re
from typing import Union, List, Tuple


class Plagiarism(object):
    def __init__(self, check_directory: str, ignored_files: Union[List[str], None] = None,
                 ignored_files_r: Union[List[str], None] = None) -> None:
        """
        Create a plagiarism object for a given directory.
        :param check_directory: Directory to check.
        :param ignored_files: List of literal file names/paths to ignore.
        :param ignored_files_r: List of regex strings to ignore files.
        """
        self.__check_directory = check_directory
        self.__ignored_files = ignored_files if ignored_files else []
        self.__ignored_files_r = ignored_files_r if ignored_files_r else []
        self.__seen_hashes = []
        self.__new_hashes = []
        self.__hash_passed_files = []

    def check_hash(self) -> Union[List[Tuple[Tuple[str, str, str], Tuple[str, str, str]]], None]:
        """
        Checks files, by hash, at the given directory
        :return: None, if no plagiarism, or list of tuples of 2-tuples of the offenders of the format: (file, hash,
        folder)
        """
        print("[Plagiarism] Checking file hashes")
        top_level_folders = [x[1] for x in os.walk(self.__check_directory)][0]
        hashlist = []
        for folder in top_level_folders:
            hashlist += self._hash_it(folder)
        results = []
        # Linear search the hashes
        for i in range(0, len(hashlist) - 1):
            if hashlist[i][1] in self.__seen_hashes:
                results.append((hashlist[i], ("", "", "Given hash")))
            # Short circuit if we have already added this hash
            if len(self.__new_hashes) and hashlist[i][1] in self.__new_hashes:
                continue
            # Search ahead for duplicates
            for j in range(i + 1, len(hashlist)):
                # Add duplicates to results
                if hashlist[i][1] == hashlist[j][1]:
                    results.append((hashlist[i], hashlist[j]))
            # Add the new hash if it is not new
            if not len(self.__new_hashes) and hashlist[i][1] not in self.__seen_hashes:
                self.__new_hashes.append(hashlist[i][1])
            elif hashlist[i][1] not in self.__new_hashes:
                self.__new_hashes.append(hashlist[i][1])
                self.__hash_passed_files.append(hashlist[i])
        return results if len(results) else None

    def check_hash_str(self) -> str:
        """
        (String version of check_hash) Checks files, by hash, at the given directory
        :return: Fancier output of check_hash as a string with instances separated by "=" bars and "-" separating files.
        Returns an empty string for no plagiarism.
        """
        results = self.check_hash()
        if results:
            results_string = "=" * 70 + "\n"
            for result in results:
                results_string += f"[Plagiarism] File: {result[0][0]}\n"
                results_string += f"[Plagiarism] Student: {result[0][2]}\n"
                results_string += "-" * 70 + "\n"
                results_string += f"[Plagiarism] File: {result[1][0]}\n"
                results_string += f"[Plagiarism] Student: {result[1][2]}\n"
                results_string += "=" * 70 + "\n"
            return results_string
        else:
            return ""

    def _hash_it(self, rel_folder) -> List[Tuple[str, str, str]]:
        file_list = []
        for root, directories, files in os.walk(self.__check_directory + os.path.sep + rel_folder):
            for filename in files:
                if filename not in self.__ignored_files:
                    relative_path = os.path.relpath(os.path.join(root, filename))
                    ignored = False
                    if len(self.__ignored_files_r):
                        for regex in self.__ignored_files_r:
                            if re.search(regex, relative_path):
                                ignored = True
                    if ignored:
                        continue
                    file_list.append(relative_path)
        return [(file, self._get_hash(file), rel_folder) for file in file_list]

    @staticmethod
    def _get_hash(file_path: str, mode="sha256") -> str:
        """
        Calculates the hash of the given file
        :param file_path: Path to the file
        :param mode: Method to calculate the hash of the file
        :returns: Hex digest of the file hash
        """
        file_hash = hashlib.new(mode)
        with open(file_path, 'rb') as file:
            data = file.read()
        file_hash.update(data)
        return file_hash.hexdigest()

    @property
    def seen_hashes(self) -> List[str]:
        """
        Get a list of all seen and new hashes
        :return: List of strings
        """
        return self.__seen_hashes + self.__new_hashes

    @seen_hashes.setter
    def seen_hashes(self, value: List[str]) -> None:
        """
        Inject old file hashes to compare against
        :param value: a list of strings of the hex digest of the sha256 sum of the files
        :return: None
        """
        self.__seen_hashes = value
