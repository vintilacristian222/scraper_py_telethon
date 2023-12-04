
# Telegram Channel Scraper Project
# Dockerized project on the way

## Project Overview

This project is designed to scrape content from Telegram channels. It consists of several components:

- `tg_scraper_for_private.py`: Main script for scraping Telegram channels.
- `web_interface.py`: A Streamlit-based web interface for interacting with the scraper.
- `afunctions.py`: Contains auxiliary functions to support the main scraper and web interface.
- `telegram_settings_v1.json`: Configuration file for setting up Telegram API credentials and other parameters.

## Requirements

- Python 3.8+
- Streamlit
- Telethon
- Requests

Install these libraries using pip:

```bash
pip install streamlit telethon requests httpx asyncio
```

## Installation Instructions

1. Clone or download the repository.
2. Install required Python libraries as listed above.

## Configuration

Configure the `telegram_settings_v1.json` with your Telegram API credentials (API ID, API hash) and other necessary settings.

## Usage Instructions

### tg_scraper_for_private.py

This script scrapes content from specified Telegram channels. Before running, ensure `telegram_settings_v1.json` is properly configured.

Run the script using:

```bash
python tg_scraper_for_private.py
```

### web_interface.py

This Streamlit application provides a web interface for the scraper.

Start the interface with:

```bash
streamlit run web_interface.py
```

Access the interface in a web browser at the address provided by Streamlit.

### afunctions.py

This file contains helper functions used by the scraper and web interface. It's imported by other scripts as needed.

## Detailed Code Explanation

Due to the complexity and length of the code, detailed explanations for each script are provided separately. Each script is annotated with comments for clarity.

---

For more information or assistance, please refer to the individual script files or contact the project maintainers.
