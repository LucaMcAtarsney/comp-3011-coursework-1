# This file contains a utility for generating unique, random player names.
# It combines adjectives and nouns to create memorable and distinct names.

import random
from typing import List

# A pool of adjectives and nouns to be combined for name generation.
ADJECTIVES = [
    "Swift", "Brave", "Mighty", "Silent", "Dark", "Mystic", "Thunder", "Shadow",
    "Frost", "Fire", "Storm", "Iron", "Golden", "Silver", "Crystal", "Wild",
    "Noble", "Ancient", "Fierce", "Clever", "Bold", "Crimson", "Azure", "Jade",
    "Phantom", "Cyber", "Cosmic", "Lunar", "Solar", "Blazing", "Frozen", "Electric",
    "Toxic", "Neon", "Venom", "Rogue", "Stealth", "Chaos", "Primal", "Savage"
]

NOUNS = [
    "Wolf", "Dragon", "Phoenix", "Tiger", "Hawk", "Bear", "Fox", "Lion",
    "Eagle", "Panther", "Viper", "Raven", "Falcon", "Cobra", "Lynx", "Shark",
    "Knight", "Warrior", "Hunter", "Ranger", "Mage", "Blade", "Arrow", "Shield",
    "Striker", "Reaper", "Slayer", "Rider", "Guardian", "Sentinel", "Champion", "Ninja",
    "Samurai", "Viking", "Spartan", "Crusader", "Paladin", "Berserker", "Assassin", "Demon"
]

def generate_random_name() -> str:
    """
    Generates a single random name by combining an adjective and a noun.
    """
    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return f"{adjective}{noun}"

def generate_unique_name(existing_names: List[str], max_attempts: int = 100) -> str:
    """
    Generates a unique random name that is not already in the provided list.
    If a unique name cannot be found after a certain number of attempts,
    it appends a number to ensure uniqueness.
    
    Args:
        existing_names: A list of names that are already in use.
        max_attempts: The maximum number of times to try generating a unique name.
    
    Returns:
        A unique random name as a string.
    """
    for _ in range(max_attempts):
        name = generate_random_name()
        if name not in existing_names:
            return name
    
    # If all attempts fail, append a number to ensure uniqueness.
    base_name = generate_random_name()
    counter = 1
    while f"{base_name}{counter}" in existing_names:
        counter += 1
    return f"{base_name}{counter}"

def get_available_name_count() -> int:
    """
    Calculates the total number of unique name combinations available.
    """
    return len(ADJECTIVES) * len(NOUNS)
