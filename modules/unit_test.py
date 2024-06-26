from modules.helpers.good_job import good_job
from modules.helpers.threadwrv import ThreadWRV
import os
import random
import re
import shutil
import subprocess
from threading import Thread
from typing import List


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
    def __init__(self, repo_directory: str, test_dir_name="test") -> None:
        """
        Create a UnitTest object to perform unit-testing of student code
        :param repo_directory: directory that the repos are in
        :param test_dir_name: (optional) Name of the test directory in the repo, default of "test"
        """
        self.__repo_directory = repo_directory
        self.__student_list: List[str] = [x[1] for x in os.walk(repo_directory)][0]
        self.__test_dir = test_dir_name

        # Figure out what this system's python command is
        if not os.system("python --version"):
            self.__py_cmd = "python"
        elif not os.system("python3 --version"):
            self.__py_cmd = "python3"
        else:
            self.__py_cmd = "py"
        print(f"[Unittest] Using python command: {self.__py_cmd}")

    @staticmethod
    def __feedback(error_count: int, failure_count: int, total: int) -> str:
        """
        Gets an appropriate feedback string.
        :param error_count: Number of errors in the unit-test run
        :param failure_count: number of failures in the unit-test run
        :param total: total number of tests in the unit-test run
        :return: feedback string
        """
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
            print(f"[Unittest] Running tests for {student}...")
            threads.append(ThreadWRV(target=self._test_thread, args=[student]))
            threads[-1].start()
            if len(threads) > 20:
                if not threads[0].is_alive():
                    result = threads[0].join()
                    if result:
                        results.append(result)
                        threads.pop(0)
        for thread in threads:
            result = thread.join()
            if result:
                results.append(result)
        for student, output in results:
            Thread(target=self._results_thread, args=[student, output]).run()

    def _test_thread(self, student):
        files = [y for y in
                 [x[2] for x in os.walk(f"{self.__repo_directory}/{student}/")][0]
                 if not y.startswith("test") and y.endswith(".py")]
        for file in files:
            with open(f"{self.__repo_directory}/{student}/{file}", "r") as code_file:
                file_data = code_file.read()
            if re.search(r"=.*?input\(.*?\)", file_data):
                print(f"![Unittest] Unable to process tests for {student}")
                return student, "Unable to process tests"
        process = subprocess.Popen(
            f"cd {self.__repo_directory}/{student}/ && {self.__py_cmd} -m unittest discover {self.__test_dir}",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        try:
            process_output = process.communicate(timeout=5)
            output = process_output[1].decode("utf-8") + process_output[0].decode("utf-8")
        except subprocess.TimeoutExpired:
            output = "Timeout expired"
            print(f"![Unittest] Test thread timeout expired for {student}")
            process.kill()
        return student, output

    def _results_thread(self, student, output):
        # Get the run summary, counting the errors, failures, and passes
        try:
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
        except IndexError:
            summary = "Something went wildly wrong. The code has spectacularly failed so hard I received no error.\n"

        # Save the run result
        result = summary + output
        with open(f"{self.__repo_directory}/{student}.txt", "wb") as output_file:
            output_file.write(result.encode('utf-8', 'ignore'))
