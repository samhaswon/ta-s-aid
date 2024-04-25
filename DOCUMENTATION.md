# Documentation

<div align="center">

Modules:

[Git](#module-git)

[ILearnZip](#module-ilearnzip)

[ImportCheck](#module-importcheck)

[Plagiarism](#module-plagiarism)

[Run](#module-run)

[UnitTest](#module-unittest)

---

Helpers:

[good_job](#helper-goodjob)

[ThreadWRV](#helper-threadwrv)

---

</div>

# Module: `Git`

## Description
The `Git` class is a simple module designed for bulk-cloning Git repositories. It provides functionality to clone repositories, retrieve the last commit date for each student's repository, and print commit summaries.

<details>

<summary>Usage</summary>

## Constructor

`__init__(self, git_url: str, use_ssh: bool = True) -> None`


Parameters:

- `git_url` (str): Base URL for the Git repositories.
- `use_ssh` (bool, default True): Indicates whether to use SSH for cloning.

## Methods

`clone(self, repo_list: List[Tuple[str, str]], destination: str = "working_dir", print_summary=True) -> List[Tuple[str, str]]`

Clones student repositories to a working directory.

Parameters:

- `repo_list` (List[Tuple[str, str]]): List of student names and repo additions that form the repository name.
- `destination` (str, default "working_dir"): Directory for cloned repositories.
- `print_summary` (bool, default True): Prints a summary of commit dates if True.

Returns: List of Tuples in the format (student, last commit date).

</details>

# Module: `ILearnZip`

## Description
The `ILearnZip` class provides functionality for extracting and manipulating iLearn zip submissions. It is intended for use with bulk downloads. It can extract, organize the submissions, and inject specific files into each student's submission directory.

Note: The current implementation breaks if a folder or file name ends in a space.

<details>

<summary>Usage</summary>

## Constructor

`__init__(self, path_to_zip: str, output_dir: str = "submissions", zip_expected: bool = True)`

Parameters:

- `path_to_zip` (str): Path to the iLearn zip file.
- `output_dir` (str, optional): Output directory for extracted submissions (default is "submissions").
- `zip_expected` (bool, default True): Indicates whether zip submissions are expected.

## Methods

`extract(self, normalize_filename: Union[str, None] = None) -> None`

Extract the contents of the iLearn zip file.

Parameters:
- `normalize_filename` (Union[str, None], optional): Name to normalize files to if provided. 
 
Returns: None

`inject(self, file: str, output: Union[str, None]) -> None`
 
Injects a given file into the student's submission directory.

Parameters:

- `file` (str): Relative path to the file to inject.
- `output` (Union[str, None], optional): Name in the student directory to inject the file as.

Returns: None

`flatten(self) -> None`

Flattens the folder structure of submission. This is useful when a zip submission is expected and students have zipped a folder and a folder. This method recursively moves the contents of folders up.

Parameters: None

Returns: None

</details>

# Module: `ImportCheck`

## Description
The `ImportCheck` class is designed for checking files in a directory for the import of a specified module. It identifies files that do not import the specified module and provides the option to add a note about the penalty for not importing the module. It is currently Python only.

<details>

<summary>Usage</summary>

## Constructor

`__init__(self, check_directory: str, penalty: str = "")`

Parameters:

- `check_directory` (str): Directory to check for imports.
- `penalty` (str, optional): Add a note about the points taken off for not importing a module.

## Methods

### `check(self, file: str, module: str, add_to_file=True) -> List[str]`
- Check files for imports of a given module.

Parameters:

- `file` (str): Name of the file to check for the import of a module.
- `module` (str): Name of the module to check for the import of.
- `add_to_file` (bool, default True): Whether to add a note to a file about the missing import.

Returns a list of files' paths without the specified import.

## Exceptions

### `Exception("No file to write to. Consider creating an output file for each folder or use the output of the function. You may consider using the unit test module for this task.")`

- Raised when attempting to add a note about imports to a file (`add_to_file=True`) but there is no file to write to.
- Consider the use of the unit test module for creating such a file.

## Example Usage
```python
from modules.import_check import ImportCheck
# Create an ImportCheck object
import_check_obj = ImportCheck(check_directory="/path/to/files", penalty="5 points off")

# Check for imports of a module in a specific file
result = import_check_obj.check(file="example.py", module="numpy")

# Print the result
print(result)
```
</details>

# Module: `Plagiarism`

## Description
The `Plagiarism` class is designed for checking file hashes in a given directory to identify potential instances of plagiarism. It calculates the hash of each file and compares them to detect similarities.

<details>

<summary>Usage</summary>

## Constructor

`__init__(self, check_directory: str, ignored_files: Union[List[str], None] = None,
                ignored_files_r: Union[List[str], None] = None) -> None`
Parameters:
- `check_directory` (str): Directory to check for plagiarism.
- `ignored_files` (Union[List[str], None], optional): List of literal file names/paths to ignore.
- `ignored_files_r` (Union[List[str], None], optional): List of regex strings to ignore files.

## Methods

`check_hash(self) -> Union[List[Tuple[Tuple[str, str, str], Tuple[str, str, str]]], None]`

- Check files by hash in the specified directory.
- Returns a list of tuples representing potential plagiarism instances.
- Each tuple contains two 3-tuples representing the files involved (file name, hash, student folder).
- Returns `None` if no plagiarism is detected.
- Results are stored as a text file in the `check_directory` with the student's name

`check_hash_str(self) -> str`

- String version of `check_hash`.
- Provides a formatted output as a string for instances of plagiarism.
- Returns an empty string for no plagiarism.
- Results are stored as a text file in the `check_directory` with the student's name

## Properties

`seen_hashes`

- Getter and setter for a list of all seen and new hashes.
- Used to retrieve and inject old file hashes for comparison.

## Example Usage
```python
from modules.plagiarism import Plagiarism


# Create a Plagiarism object
plagiarism_obj = Plagiarism(check_directory="/path/to/files", ignored_files=["ignore_me.py"])

# Check for plagiarism and print the results
print(plagiarism_obj.check_hash_str())
```
</details>

# Module: `Run`

## Description
The `Run` class is designed for executing commands in student folders. It provides the capability to run a specified command in each student's folder concurrently using threads.

<details>

<summary>Usage</summary>

## Constructor

`__init__(self, directory) -> None`

Parameters:

- `directory` (str): The directory where student folders are located.

## Methods

`run(self, command: str) -> None`

- Run the specified command in each student's folder.
- Utilize separate threads for parallel execution.
- Results are stored as a text file in the `check_directory` with the student's name

## Example Usage
```python
from modules.run import Run


# Create a Run object
run_obj = Run(directory="/path/to/student_folders")

# Run a command in all student folders
run_obj.run(command="some_command")
```

</details>

# Module: `UnitTest`

## Description
The `UnitTest` class is designed for performing unit-testing of student code in a given repository directory. It runs tests for each student in a separate thread and provides feedback on the test outcomes.

<details>

<summary>Usage</summary>

## Constructor

`__init__(self, repo_directory: str, test_dir_name="test") -> None`

Parameters:

- `repo_directory` (str): The directory containing student repositories.
- `test_dir_name` (str, optional): Name of the test directory in the student repositories (default is "test").

## Methods

`do_tests(self) -> None`

- Run all student tests in the specified directory.
- Use separate threads for each student to parallelize the testing process.
- Results are stored as a text file in the `check_directory` with the student's name

## Example Usage
```python
from modules.unit_test import UnitTest


# Create a UnitTest object
unit_test = UnitTest(repo_directory="/path/to/repositories", test_dir_name="tests")

# Run tests for all students
unit_test.do_tests()
```

</details>

# Helper: `good_job`

Returns (str) Random congratulation message

# Helper: `ThreadWRV`

Hacky solution adapted from StackOverflow for a Python Thread to return a value. It's only really useful for tasks not bound by the [GIL](https://wiki.python.org/moin/GlobalInterpreterLock).
