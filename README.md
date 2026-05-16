# Telegram Message Monitor

Python script that logs new Telegram messages from a selected user and downloads their attachments.

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

## Notes

- The script can only see messages available to your Telegram account.
- It logs only new messages received while the script is running.
- Keep `.env`, `*.session`, logs, and downloaded media private.
- Do not commit `.env` or session files to GitHub.
