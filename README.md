# Telegram stalker
Python script that logs activity from a selected Telegram user:

- new messages and downloaded attachments;
- stable online/offline changes;
- unavailable privacy statuses such as "last seen recently" or "last seen a long time ago";
- story updates visible to your Telegram account.

## Requirements

- Python 3.9+
- Telegram API credentials from <https://my.telegram.org/apps>

## Setup

1. Clone or download the project.
2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` from the example:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
API_ID=your_api_id
API_HASH=your_api_hash
```

## Run

```bash
python main.py
```

On the first run, Telegram will ask for your phone number, login code, and possibly your 2FA password. After login, enter the target username, for example:

```text
@username
```

Stop the script with `Ctrl+C`.

## Logs

For `@username`, the script creates:

- `log-username.txt` with messages, presence changes, unavailable presence notices, and story updates;
- `images-username/` for message photos;
- `voice-username/` for voice messages and video notes;
- `files-username/` for other attachments.

