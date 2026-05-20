# 🎓 AbitBot

A Telegram bot for prospective students of the Faculty of Applied Mathematics and Informatics. Helps navigate the admission process — explains specializations, answers common questions, and calculates your competitive score.

---

## ✨ Features

- 📚 Information about FAMI specializations
- 🧮 Competitive score calculator
- ❓ Answers to frequently asked questions from applicants
- 🔗 Useful links — admission campaign, schedule, contacts

---

## 🛠 Tech Stack

- **Language:** Python
- **Framework:** aiogram
- **Hosting:** Fly.io

---

## 🚀 Running with Docker

```bash
git clone https://github.com/liorenline/AbitBot.git
cd AbitBot
```

Create a `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token
```

Build and run:

```bash
docker build -t abitbot .
docker run --env-file .env abitbot
```

---

## 🔧 Running locally (without Docker)

### 1. Clone the repository

```bash
git clone https://github.com/liorenline/AbitBot.git
cd AbitBot
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root:

```env
BOT_TOKEN=your_telegram_bot_token
```

Get your token from [@BotFather](https://t.me/BotFather) on Telegram.

### 4. Run the bot

```bash
python main.py
```

---

## 📁 Project Structure

```
AbitBot/
├── main.py          # Entry point
├── handler.py       # Message & command handlers
├── keyboards.py     # Telegram keyboard layouts
├── data.py          # Specializations, FAQ, links data
├── utils.py         # Score calculator and helpers
└── requirements.txt
```
