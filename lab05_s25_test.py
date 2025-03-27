import re
import subprocess
import Levenshtein


Creative_Works_output = """
The Iliad (Homer)

Creative_Work: The Judgment of Paris
    class: Painting
    creator: Peter Paul Rubens
    date: 1635
    characters: []
    locations: National Gallery of Art, Washington, D.C., USA
    relevant_works: []
    medium: Oil on canvas
    link: https://www.nationalgallery.org.uk/paintings/peter-paul-rubens-the-judgement-of-paris
"""

Entities_output = """
Athena (God of ruled over wisdom, courage, strategic warfare)

Entity: Medusa
    class: Monster
    residence: Cisthene
    mother: Phorcys
    father: Ceto
    domain: Once a beautiful maiden, Medusa is now depicted with a hideous visage, featuring writhing snakes instead of hair and eyes that turn onlookers to stone
    roman_name:
    symbol:
    legacy:
    abilities: Medusa possesses the ability to turn anyone who gazes upon her into stone with her petrifying gaze
['Atlas', 'Epimetheus', 'Prometheus']
['Atlas', 'Crius', 'Cronus', 'Epimetheus', 'Hyperion', 'Oceanus', 'Phoebe', 'Prometheus', 'Rhea', 'Themis']
"""

Items_output = """
Talaria (owner: Hermes)

Item: Sagitta
    class: Bow and Arrow
    owner: Heracles
    description: The Arrow used by Heracles to kill Aquila, the bird that ate Prometheus' liver.
['The Caduceus', 'Winged Petasos', 'Talaria']
"""

Locations_output = """
Elysium (modern day )
Location: Crete
    class: Island
    real: TRUE
    geographical_location: Greece
    size: 3,219 square miles
    description:
Location: The Labyrinth
    class: Landmark
    real: FALSE
    geographical_location:
    size:
    description: The Labyrinth is a mythological maze created by Daedalus on the island of Crete to contain the Minotaur
"""


def is_close_enough(a: str, b: str) -> int:
    """
    Returns true if the strings are roughly similar.
    :param a: The first string to compare.
    :param b: The second string to compare.
    :return: Boolean of string similarity.
    """
    return Levenshtein.distance(
        re.sub(r"\s\s+", " ", a.lower()),
        re.sub(r"\s\s+", " ", b.lower())
    )


def run_code(filename: str) -> str:
    """
    Runs the specified Python file with `python3` as the command.
    :param filename: The file to run.
    :return: The process output.
    """
    process = subprocess.Popen(
        f"python3 {filename}",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    try:
        process_output = process.communicate(timeout=5)
        output = process_output[1].decode("utf-8") + process_output[0].decode("utf-8")
    except subprocess.TimeoutExpired:
        output = "Timeout expired"
        process.kill()
    return output


if __name__ == '__main__':
    print(f"Creative_Works.py: {is_close_enough(Creative_Works_output, run_code('Creative_Works.py'))}")
    print(f"Entities.py: {is_close_enough(Entities_output, run_code('Entities.py'))}")
    print(f"Items.py: {is_close_enough(Items_output, run_code('Items.py'))}")
    print(f"Locations.py: {is_close_enough(Locations_output, run_code('Locations.py'))}")
