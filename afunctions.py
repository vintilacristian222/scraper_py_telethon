import json
import random
import asyncio
import time
import re
import requests


# randomize time
def time_randomize():
    predefined_times_list = [500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600]
    actual_used_time = predefined_times_list[random.randint(0, len(predefined_times_list)-1)] / 1000
    return actual_used_time


# load telegram config
def load_settings_telegram():
    with open("telegram_settings_v1.json", "r") as file:
        return json.load(file)


# load discord config
def load_settings_discord():
    with open("discord_settings.json", "r") as file:
        return json.load(file)


# Function to periodically reload settings
async def reload_settings(settings_telegram, settings_discord):
    last_checked = time.time()
    while True:
        await asyncio.sleep(10)  # Check for updates every 10 seconds
        if time.time() - last_checked > 10:
            new_settings_telegram = load_settings_telegram()
            new_settings_discord = load_settings_discord()
            settings_telegram.update(new_settings_telegram)
            settings_discord.update(new_settings_discord)
            last_checked = time.time()


def check_sender_username(event):
    if event.sender:
        if event.sender.username:
            username_to_send_to_discord = event.sender.username
        else:
            # Construct sender name from first name and last name, if available
            first_name = event.sender.first_name if event.sender.first_name else ""
            last_name = event.sender.last_name if event.sender.last_name else ""
            username_to_send_to_discord = f"{first_name} {last_name}".strip()
    else:
        username_to_send_to_discord = "Unknown Sender"

    return username_to_send_to_discord


# check  username to match allowed authors
def check_author(username_to_send_to_discord, allowed_authors):
    if not allowed_authors:  # If allowed_authors is empty or not specified, consider all authors
        is_author_allowed = True
    else:
        is_author_allowed = any(author.lower() == username_to_send_to_discord.lower() for author in allowed_authors)

    return is_author_allowed


# check message content to match specific words
def match_message_to_specific_word(specific_words, word_pattern, message_content):
    if specific_words:
        found_specific_words = [word for word in specific_words if
                                re.search(word_pattern.format(word), message_content)]
    else:
        found_specific_words = [message_content]  # Consider all messages if specific_words is empty

    return found_specific_words


