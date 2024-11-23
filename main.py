import os
import random
import threading
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

#==========Web server==========
from status_web import start_http_server

server_thread = threading.Thread(target=start_http_server, daemon=True)
server_thread.start()
#==========================
load_dotenv()
#==========MongoDB (database)==========
from pymongo.mongo_client import MongoClient  # noqa: E402

uri = os.getenv('MONGODB_CONNECTION')

client = MongoClient(uri)
config_collection = client["configs"]["servers"]

try:
    client.admin.command('ping')
    print("Successfully connected to MonoDB!")
except Exception as e:
    print(e)

def write_to_config_simple(server_id: int, **kwargs) -> None:
    data = {}
    data[id] = server_id
    for key, value in kwargs.items():
        data[key] = value
    config_collection.insert_one(data)

#===========================================
TOKEN = os.getenv('APP_TOKEN')

intents = discord.Intents()
intents.messages = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(intents=intents)

#====================Slash commands====================

#=====Dicing=====
dicing_random_responses = ["Look at that, it's [] !", " Ooh, it's []!", "Hmm.. Looks like you rolled []!", "Let's say.. []!", "Lemme see. It's []!", "Dicing.. []!", "Rolling, rolling, []!"]

@bot.slash_command(description="Roll a dice")
async def roll_a_dice(ctx: discord.ApplicationContext):
    response = dicing_random_responses[random.randint(0, len(dicing_random_responses) - 1)].replace("[]", "`" + str(random.randint(1, 6)) + "`")
    await ctx.respond(response)

@bot.slash_command(description="Roll a custom dice")
async def roll_custom_dice(ctx: discord.ApplicationContext, dices):
    try:
        dices = int(dices)
        if dices <= 1:
            await ctx.respond("Invalid dice value")
        else:
            response = dicing_random_responses[random.randint(0, len(dicing_random_responses) - 1)].replace("[]", "`" + str(random.randint(1, dices)) + "`")
            await ctx.respond(response)
    except ValueError:
        await ctx.respond("Invalid number")
#=====Skullboard=====

#====Guess the number====
@bot.slash_command(description = "Guess the number from 1-10")
async def guess_the_number(ctx: discord.ApplicationContext, guess):
    try:
        if not 0 < int(guess) < 11:
            await ctx.respond("Invalid guess. Must be a number from 1-10")
        else:
            if random.randint(1,10) == int(guess):
                await ctx.respond("Correct!!")
            else:
                await ctx.respond("Better luck next time lol")
    except ValueError:
        await ctx.respond("Invalid number")
#=====================================================


#==========Events==========
@bot.event
async def on_ready():
    time.sleep(0.5)
    print(f'"{bot.user.name}" is now ready!')
    activity = discord.Activity(name="`/help`",
                                type=discord.ActivityType.listening,
                                buttons=[{"label": "Open source", "url": "https://github.com/Tony14261/MicroMightyBot/"}, {"label": "Status", "url": "https://stats.uptimerobot.com/4CoTZy3oIe"}])
    await bot.change_presence(status=discord.Status.online,
                              activity=activity)

@bot.event
async def on_connect():
    try:
        await bot.sync_commands()
        print(f"{bot.user.name} connected.")
    except discord.HTTPException as e:
        print(f"Failed to sync commands: {e}")

#==========================

#=================================================================================================================================

def main():
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
