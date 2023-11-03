import os
from typing import List


class ImportCheck(object):
    def __init__(self, check_directory: str):
        """
        :param check_directory: Directory to check for imports
        """
        self.__check_directory = check_directory

    def check(self, file: str, module: str, add_to_file=True) -> List[str]:
        """
        Check files for imports of a given module
        :param file: Name of the file to check for the import of a module
        :param module: name of the module to check for the import of
        :param add_to_file: (default True) whether to ADD "You did not import (and therefore did not use) {module}\n" to
        the start of the file. Requires there being a file to add to from something like the unit_test module.
        :return: List of files' path without the import
        """
        folders = [x[1] for x in os.walk(self.__check_directory)][0]
        no_import_list = []

        for folder in folders:
            for root, directories, files in os.walk(self.__check_directory + os.path.sep + folder):
                for filename in files:
                    if filename == file:
                        path = os.path.relpath(os.path.join(root, filename))
                        with open(path, "r") as sub_file:
                            contents = sub_file.read()
                        if f"import {module}" not in contents and f"from {module} import" not in contents:
                            if add_to_file:
                                with open(self.__check_directory + os.path.sep + f"{folder}.txt", "r") as feedback_file:
                                    feedback = feedback_file.read()
                                contents = f"You did not import (and therefore did not use) {module}\n" + feedback
                                with open(self.__check_directory + os.path.sep + f"{folder}.txt", "w") as feedback_file:
                                    feedback_file.write(contents)
                            no_import_list.append(path)
        return no_import_list
