import random


def good_job() -> str:
    """
    Random congratulation message
    :return: (string) congratulation message
    """
    congratulations = [
        "Brilliant job!",
        "Code executed successfully!",
        "Everything looks great!",
        "Excellent work!",
        "Exceptionally bug-free code!",
        "Fantastic!",
        "Good job!",
        "Great job!",
        "Good work!",
        "Keep it up!",
        "Keep up the good work!",
        "Nice work!",
        "Syntax Error Free!",
        "That's some top-notch work!",
        "That's the way to go!",
        "Well done!",
        "You did great!",
        "You did well.",
        "You nailed it!",
        "You're doing a great job!",
        "You've outdone yourself!",
        "Your code is error-free!",
        "Your code is running smoothly!",
        "Your code works perfectly!"
    ]
    return random.choice(congratulations)
