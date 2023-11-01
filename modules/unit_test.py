from modules.good_job import good_job
import os
import random
import shutil
import subprocess
from threading import Thread
from typing import List


class ThreadWRV(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def some_failure_feedback() -> str:
    feedback = [
        "Some of your tests failed.",
        "Some of your tests have not passed successfully.",
        "There were failures in some of your tests.",
        "Not all of your tests have passed.",
        "Your code did not pass all of the tests.",
        "A few tests have failed in your code.",
        "Your code did not achieve success in all tests.",
        "Some test cases have returned failures.",
        "There are test failures in your code.",
        "Your code did not meet the criteria in some of the tests.",
        "Certain tests did not produce the expected results.",
        "A portion of your tests did not pass.",
        "Your code didn't succeed in all tests.",
        "There are issues with certain test outcomes.",
        "Not all test cases returned the expected results.",
        "Your code fell short in a few tests.",
        "Some test scenarios did not produce the desired results.",
        "A subset of your tests did not meet the criteria.",
        "Your code didn't fully pass all the required tests.",
        "Some tests didn't go as planned in your code.",
    ]
    return random.choice(feedback)


def some_error_feedback() -> str:
    feedback = [
        "Your tests produced errors without any failures.",
        "Errors were encountered during the execution of your tests.",
        "There were no test failures, but errors were present in your code.",
        "Only errors were identified in your test results.",
        "No test failures, but errors were found in your tests.",
        "Your code ran into errors without any test failures.",
        "Errors were the only issues in your test outcomes.",
        "Your code didn't produce test failures, but it did generate errors.",
        "Only errors were observed during the test execution.",
        "No test failures, but errors were detected in your code.",
        "Errors, but no test failures, were present in your code.",
        "Your code encountered errors without any test issues.",
        "Errors were the sole problem in your test results.",
        "Your tests encountered errors.",
        "Errors were the only issues in your test outcomes.",
        "No test failures, but errors were the challenge in your code.",
        "Only errors were detected in your test results.",
    ]
    return random.choice(feedback)


def some_failure_and_error_feedback() -> str:
    feedback = [
        "Your tests resulted in a mix of failures and errors.",
        "There's a combination of test failures and errors in your code.",
        "Your code encountered both test failures and errors.",
        "You have a mixture of test failures and errors in your code.",
        "A blend of test failures and errors was found in your tests.",
        "Your code produced a mix of test failures and errors.",
        "Both test failures and errors were observed in your code.",
        "You're dealing with a combination of test failures and errors.",
        "Some of your tests failed, and others encountered errors.",
        "A combination of test failures and errors is present in your code.",
        "Your tests exhibited a mix of both failures and errors.",
        "A combination of test failures and errors has been identified in your code.",
        "Your code displayed a mixture of test failures and errors.",
        "You've experienced both test failures and errors in your code.",
        "A mix of test failures and errors was found in your tests.",
        "There's a blend of test failures and errors in your code."
    ]
    return random.choice(feedback)


def all_failed() -> str:
    feedback = [
        "Unfortunately, none of your tests passed successfully.",
        "Your code did not meet the criteria in any of the tests.",
        "All test cases resulted in failure in your code.",
        "None of the tests produced the expected results.",
        "Regrettably, your code failed all the tests.",
        "There were no successful test outcomes in your code.",
        "Every single test encountered issues in your code.",
        "None of your tests yielded positive results.",
        "Your code did not pass a single test successfully.",
        "All tests ended in failure in your code.",
        "No test cases achieved success in your code.",
        "Your code did not meet the criteria in any of the tests.",
        "Unfortunately, all tests failed in your code.",
        "Not a single test case returned the expected results.",
        "Your code did not achieve success in any tests.",
        "There were no passing test outcomes in your code.",
        "All tests exhibited issues in your code.",
        "None of your tests met the criteria for success.",
        "Your code did not succeed in any of the tests.",
        "All tests failed to meet the expected results in your code.",
        "Your code did not meet the criteria, and none of the tests passed successfully"
    ]
    return random.choice(feedback)


class UnitTest(object):
    def __init__(self, student_list: List[str], repo_directory: str, test_dir_name="test") -> None:
        """
        Create a UnitTest object to perform unit-testing of student code
        :param student_list: List of student IDs that are used as the name of folders for their repos
        :param repo_directory: directory that the repos are in
        :param test_dir_name: (optional) Name of the test directory in the repo, default of "test"
        """
        self.__repo_directory = repo_directory
        self.__student_list = student_list
        self.__test_dir = test_dir_name

        # Figure out what this system's python command is
        if not os.system("python3 --version"):
            self.__py_cmd = "python3"
        elif not os.system("python --version"):
            self.__py_cmd = "python"
        else:
            self.__py_cmd = "py"
        print(f"Using python command: {self.__py_cmd}")

    def __feedback(self, error_count: int, failure_count: int, total: int) -> str:
        if (failure_count + error_count) == total:
            return all_failed()
        if error_count and failure_count:
            return some_failure_and_error_feedback()
        elif failure_count:
            return some_failure_feedback()
        elif error_count:
            return some_error_feedback()
        else:
            return good_job()

    def do_tests(self) -> None:
        """
        Run all student tests in a given directory
        :return: None
        """
        results = []
        threads = []
        for student in self.__student_list:
            print(f"Running tests for {student}")
            threads.append(ThreadWRV(target=self.test_thread, args=[student]))
            threads[-1].start()
        for thread in threads:
            results.append(thread.join())
        for student, output in results:
            """
            # Get the run summary, counting the errors, failures, and passes
            run_result = output.splitlines()[0]
            error_count = run_result.count("E")
            failure_count = run_result.count("F")
            pass_count = run_result.count(".")
            total = error_count + failure_count + pass_count

            # Add a summary to the output file
            summary = \
                self.__feedback(error_count, failure_count, total) + "\n" + \
                f"Errors: {error_count}\n" + \
                f"Failures: {failure_count}\n" + \
                f"Passed: {pass_count}\n" + \
                f"Total: {total}\n" + \
                "=" * shutil.get_terminal_size((70, 20)).columns + "\n\n"

            # Save the run result
            with open(f"{self.__repo_directory}/{student}.txt", "w") as output_file:
                output_file.write(summary + output)
            """
            Thread(target=self.results_thread, args=[student, output]).run()

    def test_thread(self, student):
        output = subprocess.Popen(
            f"cd {self.__repo_directory}/{student}/ && {self.__py_cmd} -m unittest discover {self.__test_dir}",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()[1].decode("utf-8")
        return student, output

    def results_thread(self, student, output):
        # Get the run summary, counting the errors, failures, and passes
        run_result = output.splitlines()[0]
        error_count = run_result.count("E")
        failure_count = run_result.count("F")
        pass_count = run_result.count(".")
        total = error_count + failure_count + pass_count

        # Add a summary to the output file
        summary = \
            self.__feedback(error_count, failure_count, total) + "\n" + \
            f"Errors: {error_count}\n" + \
            f"Failures: {failure_count}\n" + \
            f"Passed: {pass_count}\n" + \
            f"Total: {total}\n" + \
            "=" * shutil.get_terminal_size((70, 20)).columns + "\n\n"

        # Save the run result
        with open(f"{self.__repo_directory}/{student}.txt", "w") as output_file:
            output_file.write(summary + output)
