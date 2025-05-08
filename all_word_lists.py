import json
import os

pass_str = ''
dividers = '!@#$%^&*_+=-/<>?|~'

# List of prompts to be used in the game
prompt_list = [
    "Name a city",
    "Name an animal",
    "Pick a color",
    "Name a noun",
    "Name a proper noun",
    "Pick an adjective",
    "Name a food",
    "Pick a month",
    "Pick an element",
]

with open(os.path.join(os.getcwd(), 'word_lists/words.json'), 'r') as file:
    word_list = json.load(file)

with open(os.path.join(os.getcwd(), 'word_lists/adjectives.txt'), 'r') as f:
    adjectives = f.read().splitlines()
    adjectives = [i.strip('\t') for i in adjectives]
    adjectives = list(set(adjectives))

with open(os.path.join(os.getcwd(), 'word_lists/verbs.txt'), 'r') as f:
    verbs = f.read().splitlines()
    verbs = [i.strip('\t') for i in verbs]
    verbs = list(set(verbs))

with open(os.path.join(os.getcwd(), 'word_lists/science.txt'), 'r') as f:
    science = f.read().splitlines()
    science = [i.strip('\t') for i in science]
    science = list(set(science))

with open(os.path.join(os.getcwd(), 'word_lists/animals.txt'), 'r') as f:
    animals = f.read().splitlines()
    animals = [i.strip('\t') for i in animals]
    animals = list(set(animals))

with open(os.path.join(os.getcwd(), 'word_lists/colors.txt'), 'r') as f:
    colors = f.read().splitlines()
    colors = [i.strip('\t') for i in colors]
    colors = list(set(colors))