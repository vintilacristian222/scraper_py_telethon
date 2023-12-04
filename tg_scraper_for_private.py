import asyncio
from telethon import TelegramClient, events
import logging
import httpx
import afunctions as fct
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load settings with error handling
try:
    settings_discord = fct.load_settings_discord()
    settings_telegram = fct.load_settings_telegram()
    telegram_api_id = settings_telegram["telegram_api_id"]
    telegram_api_hash = settings_telegram["telegram_api_hash"]
except Exception as e:
    logging.error(f"An error occurred: {e}\n{traceback.format_exc()}")
    exit(1)

# Initiate telegram session
try:
    client = TelegramClient('session_name', telegram_api_id, telegram_api_hash)
except Exception as e:
    logging.error(f"Error initiating TelegramClient: {e}")
    exit(1)

# Word pattern
word_pattern = r'\b(?:{})\b'

# Global variables
processed_message_ids = set()

async def main():
    try:
        await client.start()
        client.loop.create_task(fct.reload_settings(settings_telegram, settings_discord))
    except Exception as e:
        logging.error(f"An error occurred: {e}\n{traceback.format_exc()}")
        return

    async def handle_new_message(event):
        try:
            settings = fct.load_settings_telegram()
            await process_message(event, settings)
        except Exception as e:
            logging.error(f"An error occurred: {e}\n{traceback.format_exc()}")

    for channel_config in settings_telegram["channels"]:
        client.add_event_handler(handle_new_message, events.NewMessage(chats=channel_config["source_channel_id"]))

    logging.info("Client started. Listening for messages from the specified channels...")
    await client.run_until_disconnected()

async def process_message(event, settings):
    # Extract message details
    message_id = event.message.id
    channel_id = event.message.chat_id
    message_content = event.message.text.lower()
    unique_message_identifier = (channel_id, message_id)

    # Find the channel configuration that matches the channel_id
    channel_config = next((c for c in settings["channels"] if str(channel_id) == c["channel_browser_id"]), None)
    if not channel_config:
        logging.warning(f"Channel configuration not found for channel ID: {channel_id}")
        return

    # Extracting channel settings
    specific_words = channel_config.get("specific_words", [])
    allowed_authors = channel_config.get("authors", [])
    channel_alias = channel_config.get("alias", "")

    found_specific_words = fct.match_message_to_specific_word(specific_words, word_pattern, message_content)
    username_to_send_to_discord = fct.check_sender_username(event)
    is_author_allowed = fct.check_author(username_to_send_to_discord, allowed_authors)
    is_not_processed = unique_message_identifier not in processed_message_ids

    if found_specific_words and is_not_processed and is_author_allowed:
        try:
            send_url = f'https://discord.com/api/v10/channels/{settings_discord["destination_channel_id"]}/messages'
            words_list = ', '.join(found_specific_words)
            payload = {
                'content': (
                    f"**From**: {channel_alias}\n"
                    f"**User**: {username_to_send_to_discord}\n"
                    f"**Message**: {message_content}\n"
                    f"**Keywords**: {words_list}\n"
                    "--------------------------------------------------\n"
                )
            }
            async with httpx.AsyncClient() as client:
                send_response = await client.post(send_url, headers={'Authorization': f'{settings_discord["discord_personal_token"]}'}, json=payload)
            if send_response.status_code == 200:
                logging.info(f'Message sent to channel {settings_discord["destination_channel_id"]}')
            else:
                logging.error(f'Failed to send message. Status code: {send_response.status_code}')
        except Exception as e:
            logging.error(f"An error occurred: {e}\n{traceback.format_exc()}")

        processed_message_ids.add(unique_message_identifier)

        await asyncio.sleep(fct.time_randomize())  # Replace time.sleep with asyncio.sleep

# Run the client
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
