import os
import re
import subprocess
import time

if __name__ == '__main__':
    with open("student.py", "r") as student_file_in:
        student_file = student_file_in.read()
        student_file = re.sub(r"except\sKeyboardInterrupt:",
                              "except NameError:  # Changed by script from KeyboardInterrupt",
                              student_file)

    with open("student.py", "w") as student_file_out:
        student_file_out.write(student_file)

    if not os.system("python --version"):
        py_cmd = "python"
    elif not os.system("python3 --version"):
        py_cmd = "python3"
    else:
        py_cmd = "py"

    output = ""

    os.rename("students.json", "student.json")

    # Start the child process
    process = subprocess.Popen(f"{py_cmd} student.py",
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               shell=True)

    missing_file = process.communicate()

    output += f"Missing file: {missing_file[0].decode()}\n\tstderr: {missing_file[1].decode()}\n"

    os.rename("student.json", "students.json")

    process.kill()

    # Restart the process
    # if process.poll() or process.poll() == 0:
    process = subprocess.Popen(f"{py_cmd} student.py",
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               shell=True)

    # Read the prompt
    os.read(process.stdout.fileno(), 4096)
    # Write two, an invalid input
    os.write(process.stdin.fileno(), "two\n".encode())
    # See what is given
    value_error = os.read(process.stdout.fileno(), 4096).decode('utf-8')

    # If the exception was not handled, restart the process
    if process.poll() or process.poll() == 0:
        output += "Restarted on ValueError\n"
    process.kill()
    process = subprocess.Popen(f"{py_cmd} student.py",
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               shell=True)

    # Give the output of the ValueError
    output += f"1st Value error: {value_error.splitlines()[0]}\n"

    """
    # Continue on to the next prompt
    # if not value_error.endswith('Enter the index of the student: '):
    os.read(process.stdout.fileno(), 4096)
    os.write(process.stdin.fileno(), "25\n".encode())
    time.sleep(0.01)
    index_error = os.read(process.stdout.fileno(), 4096).decode("utf-8")

    # If the exception was not handled, restart the process
    if process.poll():
        output += "Restarted on IndexError\n"
    process.kill()
    process = subprocess.Popen(f"{py_cmd} student.py",
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               shell=True)

    # Give the output of the IndexError
    try:
        output += f"Index error: {index_error.splitlines()[0]}\n"
    except IndexError:
        output += f"Index error: {index_error}\n"
    """

    # Read the prompt (if necessary)
    # if not index_error.endswith("Enter the index of the student: "):
    os.read(process.stdout.fileno(), 4096)
    # Write 2, a valid input
    os.write(process.stdin.fileno(), "2\n".encode())
    time.sleep(0.01)
    # Read the prompt
    os.read(process.stdout.fileno(), 4096)
    # Write zeroth, an invalid input
    os.write(process.stdin.fileno(), "zeroth\n".encode())
    time.sleep(0.01)
    days_value_error = os.read(process.stdout.fileno(), 4096).decode()

    # If the exception was not handled, restart the process
    if process.poll():
        output += "Restarted on second ValueError\n"
    process.kill()
    process = subprocess.Popen(f"{py_cmd} student.py",
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               shell=True)
    # if input is improperly handled, restart
    # if days_value_error == "How many days has the student attended school this year? ":
    #    output += "Restarted on invalid input handling for ValueError\n"
    output += f"2nd Value error: {days_value_error.splitlines()[0]}\n"

    # Read the prompt
    if not days_value_error.endswith("Enter the index of the student: "):
        os.read(process.stdout.fileno(), 4096)
    # Write 2, a valid input
    os.write(process.stdin.fileno(), "2\n".encode())
    time.sleep(0.01)
    # Read the prompt
    os.read(process.stdout.fileno(), 4096)
    # Write 0, an invalid input
    os.write(process.stdin.fileno(), "0\n".encode())
    time.sleep(0.01)
    # Read the prompt
    os.read(process.stdout.fileno(), 4096)
    # Give something
    os.write(process.stdin.fileno(), "300\n".encode())
    time.sleep(0.01)
    zero_div_error = os.read(process.stdout.fileno(), 4096).decode()

    # If the exception was not handled, restart the process
    if process.poll():
        output += "Restarted on ZeroDivisionError\n"
    try:
        output += f"Zero division error: {zero_div_error.splitlines()[0]}\n"
    except IndexError:
        output += f"Zero division error: {zero_div_error}\n"

    # Kill the child if it is still running
    if process.poll() is None:
        process.kill()

    with open("student.py", "r") as student_file_in:
        student_file = student_file_in.read()

    x = len(re.findall(r"except Exception|except:", student_file))
    output += f"Used general exceptions {x} time{'s' if x > 1 or x == 0 else ''}\n"

    fnf = len(re.findall(r"except FileNotFoundError:", student_file))
    output += f"Used FileNotFoundError {fnf} time{'s' if fnf > 1 or fnf == 0 else ''}\n"

    ve = len(re.findall(r"except ValueError:", student_file))
    output += f"Used ValueError {ve} time{'s' if ve > 1 or ve == 0 else ''}\n"

    ie = len(re.findall(r"except IndexError:", student_file))
    output += f"(ungraded) Used IndexError {ie} time{'s' if ie > 1 or ie == 0 else ''}\n"

    zde = len(re.findall(r"except ZeroDivisionError:", student_file))
    output += f"Used ZeroDivisionError {zde} time{'s' if zde > 1 or zde == 0 else ''}\n"

    print(output)
