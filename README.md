# MicroMightyBot

MicroMightyBot is a lightweight Discord bot packed with small, kinda-useless features designed to make you server more entertaining.

[Invite link](https://discord.com/oauth2/authorize?client_id=1300829284268507197)

---

## ✨ Features
- **/roll_a_dice**: Rolls a dice (outputs a random number from 1-6)
- **/roll_custom_dice**: Rolls a custom dice (outputs a random number from a custom range)
- **/guess_the_number**: Guess the number from 1-10 (see if user's input is the same as the bot's random number)

## 📚 Programs Used 
- **Language**: [Python 3.12+](https://www.python.org/)
- **Database**: [MongoDB Atlas](https://www.mongodb.com/atlas)
- **Hosting**: [Render](https://www.render.com/)

The best thing is, I am maintaining this bot for completely free, using the above programs!

## 🛠️ Remix Guide
- Warning: This project is under [CC-BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/)
### Prerequisites
- Python 3.11+ installed
- MongoDB Atlas connection string ([Get Started](https://www.mongodb.com/atlas/database))
- Discord bot token ([Create Your Bot](https://discord.com/developers/applications))

### 1. **Clone this repository**:
```bash
git clone https://github.com/Tony14261/MicroMightyBot/
```

### 2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### 3. **Set up environment variables:** Create a `.env` file in the project directory:
```python
DISCORD_TOKEN=your_discord_bot_token
MONGO_URI=your_mongodb_connection_string
```

### 4. Modify the code:
- Change the code to your style. Maybe add some features, improve the code, fix bugs,...
### 5. Set up bot on Render (for free)
- Create a web service of the project
- Start command: ```python main.py```
