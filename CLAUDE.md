# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A LINE bot that scrapes rental listings from 591.com.tw (Taiwanese rental site). Users send Chinese-language commands to the bot; the bot fetches and returns matching listings.

## Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Required environment variables
export LINE_CHANNEL_SECRET=<your_secret>
export LINE_CHANNEL_ACCESS_TOKEN=<your_token>

# Run locally
python app.py

# Run as Heroku would (via Procfile)
gunicorn app:app
```

To test the scraper without LINE:
```bash
python3 test_search.py
```

## Architecture

**`app.py`** — Flask app with a single `/callback` POST endpoint. Validates LINE webhook signatures and dispatches `MessageEvent` to `handle_message`. Parses space-separated commands like:
```
591 位置=蘆洲區 類型=獨立套房 租金=5000,15000
```

**`rent591.py`** — All 591.com.tw scraping logic:
- `theEnum`: maps user-facing Chinese param names (`位置`, `類型`, `租金`, `坪數`) to API keys
- `region` / `section` dicts: hardcoded lookup tables mapping city/district names to numeric IDs used by the 591 API
- `kind` dict: maps rental type names to 591 kind IDs
- `get_arguments_content()`: converts parsed user args into a 591 API query string (`regionid`, `sectionid`, `kind`, `rentprice`, `area`)
- `rent_591_object_list()`: establishes a fresh session by visiting the main page (to get a valid `T591_TOKEN` cookie), then hits `https://bff-house.591.com.tw/v3/web/rent/list`, returns items
- `rent_591_object_list_tostring()`: formats top 5 results into a LINE text message

**`test_search.py`** — Quick manual test script. Run `python3 test_search.py` to verify scraping without needing LINE.

## Deployment

Deployed to Heroku. The `Procfile` specifies `gunicorn app:app`. LINE webhook URL must be set to `https://<heroku-app>.herokuapp.com/callback`.
