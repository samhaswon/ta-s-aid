import random


def good_job() -> str:
    """
    Random congratulation message
    :return: (string) congratulation message
    """
    congratulations = [
        "Good job!",
        "Good work!",
        "Well done!",
        "Excellent work!",
        "Fantastic!",
        "You did great!",
        "You did well.",
        "Keep up the good work!",
        "You're doing a great job!",
        "That's the way to go!",
        "Keep it up!",
        "Nice work!",
        "You nailed it!",
        "Brilliant job!",
        "That's some top-notch work!",
        "You've outdone yourself!",
        "Code executed successfully!",
        "Your code works perfectly!",
        "Syntax Error Free!",
        "Exceptionally bug-free code!",
        "Your code is running smoothly!",
        "Your code is error-free!"
    ]
    return random.choice(congratulations)
