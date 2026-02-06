"""
Name pool utility for generating random player names
"""
import random
from typing import List

# Pool of random names combining adjectives and nouns
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
    Generate a random name by combining an adjective and a noun
    """
    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return f"{adjective}{noun}"

def generate_unique_name(existing_names: List[str], max_attempts: int = 100) -> str:
    """
    Generate a unique random name that doesn't exist in the provided list
    
    Args:
        existing_names: List of names already in use
        max_attempts: Maximum number of attempts to generate a unique name
    
    Returns:
        A unique random name
    
    Raises:
        ValueError: If unable to generate a unique name after max_attempts
    """
    for _ in range(max_attempts):
        name = generate_random_name()
        if name not in existing_names:
            return name
    
    # If we couldn't find a unique name, append a number
    base_name = generate_random_name()
    counter = 1
    while f"{base_name}{counter}" in existing_names:
        counter += 1
    return f"{base_name}{counter}"

def get_available_name_count() -> int:
    """
    Calculate the total number of possible name combinations
    """
    return len(ADJECTIVES) * len(NOUNS)
