# Please suggest and give feedbacks respectfully :)
# Under CC-BY-NC-SA (https://creativecommons.org/licenses/by-nc-sa/4.0/)

import os
import random
import threading
import time

import discord
from discord.commands import option

#from discord.ext import commands
from dotenv import load_dotenv

from exceptions import InvalidMethod, UnknownError

#==========Web server==========
from status_web import start_http_server

server_thread = threading.Thread(target=start_http_server, daemon=True)
server_thread.start()
#==============================

load_dotenv() #Load the .env file

#==========MongoDB (database)==========
from pymongo.mongo_client import MongoClient  # noqa: E402

uri = os.getenv('MONGODB_CONNECTION')

client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Successfully connected to MonoDB!")
except Exception as e:
    print(e)


#The functions are made mainly for doing actions easier
def write_to_db_one(server_id: str, collection: str, **kwargs) -> None:
    """
    Adds a data/document to the MongoDB
    - server_id: str | The discord server ID
    - collection: str | The name of the collection you want to add data to
    - **kwargs | Data you want to add to the db
    """
    client_collection = client["data"][collection]
    data = {}
    data["_id"] = server_id
    for key, value in kwargs.items():
        data[key] = value
    client_collection.insert_one(data)
def update_db_one(server_id: str, collection: str, bkeys: str=None, upsert: bool = True, method = "set", **kwargs) -> None:
    """
    Updata a data (in a document) in the MongoDB
    - `server_id`: str | The discord server ID
    - `collection`: str | The collection you want to connect
    - `bkeys`: str | More advanced. The keys you want to access before changing the value (read example below)
        - Example:
            - For example you data is like: ```{message: {content: "Hello", count2: 4, logs :{message_count: 1}}}```
            - So to update the *message_count* by 1, set `bkeys = message.logs`  `method = "inc"`  `message_count = 1`
            - To update *count2* by 1, set `bhkeys = message` `method = "inc"` `count2 = 1`
            - More info: https://www.mongodb.com/docs/manual/core/document/#dot-notation
    - `upsert`: bool | Whether you want to use upsert for the commend (adds a new value when not found)
        - Default value: True
    - `method`: str | The method you want to use
        - Default value: "set"
        - Only accepts "set" and "inc" (inc use below in "How to make your value add n")
        - "set": Set your key to a value 
        - "inc": Make you value add/subtract. More information: https://www.mongodb.com/docs/manual/reference/operator/update/inc/#behavior
    
    How to make your value add `n`:
    - Set `method = "inc"`
    - `your_key = n` 
        - *your_key* is the key you want to update
        - *n* is number you want your value to increase
        - Basically, it will be like `your_key += n`
    """
    client_collection = client["data"][collection]
    data = {}
    for key, value in kwargs.items():
        if bkeys is not None:
            data[f"{bkeys}.{key}"] = value
        else:
            data[key] = value
    if not (method == "set" or method == "inc"):
        raise InvalidMethod
    try:
        client_collection.update_one({'_id':server_id}, {f"${method}": data}, upsert=upsert)
    except Exception as e:
        raise(e)
def get_data(server_id: str, collection: str):
    """
    Returns the whole document that has the `_id = server_id` (dictionary type)
    """
    client_collection = client["data"][collection]
    return client_collection.find_one({"_id": server_id})
def delete_data_one(server_id : str, collection: str) -> None:
    """
    Deletes the whole document that has the `_id = server_id`
    """
    client_collection = client["data"][collection]
    client_collection.delete_one({"_id": server_id})

#===========================================
TOKEN = os.getenv('APP_TOKEN')

intents = discord.Intents()
intents.messages = True
intents.message_content = True
intents.presences = True
intents.guilds = True
bot = discord.Bot(intents=intents)
#bot = commands.Bot(intents=intents)

#====================Slash commands====================
@bot.slash_command(description="Get help")
async def help(ctx: discord.ApplicationContext):
    await ctx.respond( "## MicroMightyBot help\n"
                    "- `/msgcount` Features to track number of messages members sent\n"
                    "   - You could do `/msgcount guide` to view its commands\n"
                    "- `/roll_a_dice`: Rolls a dice (outputs a random number from 1-6)\n"
                    "- `/roll_custom_dice`: Rolls a custom dice (outputs a random number from a custom range)\n"
                    "- `/guess_the_number`: Guess the number from 1-10 (see if user's input is the same as the bot's random number)\n"
                     )
#=====Dicing=====
dicing_random_responses = ["Look at that, it's [] !", " Ooh, it's []!", "Hmm.. Looks like you rolled []!", "Let's say.. []!", "Lemme see. It's []!", "Dicing.. []!", "Rolling, rolling, []!"]

@bot.slash_command(description="Roll a dice")
async def roll_a_dice(ctx: discord.ApplicationContext):
    response = dicing_random_responses[random.randint(0, len(dicing_random_responses) - 1)].replace("[]", "`" + str(random.randint(1, 6)) + "`")
    await ctx.respond(response)

@bot.slash_command(description="Roll a custom dice")
@option(
    "dices",
    description="The amount of dices you want to roll",
    required=True,
)
async def roll_custom_dice(ctx: discord.ApplicationContext, dices: int):
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
@option(
    "guess",
    description="Write your guess",
    required=True,
)
async def guess_the_number(ctx: discord.ApplicationContext, guess: int):
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
    activity = discord.Activity(name="/help",
                                type=discord.ActivityType.listening,
                                buttons=[{"label": "Open source", "url": "https://github.com/Tony14261/MicroMightyBot/"}, {"label": "Status", "url": "https://stats.uptimerobot.com/4CoTZy3oIe"}])
    await bot.change_presence(status=discord.Status.online,
                              activity=activity)
    #await bot.register_command()

@bot.event
async def on_connect():
    try:
        await bot.sync_commands()
        print(f"{bot.user.name} connected.")
    except discord.HTTPException as e:
        print(f"Failed to sync commands: {e}")

#==========================

#==========Optional Features==========
#===Message Count===
staffs = [357638580530708480, 1254854714743455754, 1296457844140539954, 973091747418755092, 1307083823380693075]

@bot.event
async def on_message(message: discord.Message):
    if message.guild.id == 1303613693707288617:
        if int(message.author.id) in staffs:
            srv_id = str(message.guild.id)
            usr_id = str(message.author.id)

            client_collection = client["data"]["message_count"]
            data = {}
            data[f"{usr_id}"] = 1
            client_collection.update_one({'_id':srv_id}, {"$inc": data}, upsert=True)

@bot.event
async def on_guild_remove(guild: discord.Guild):
    delete_data_one(server_id=str(guild.id), collection="message_count")
    delete_data_one(server_id=str(guild.id), collection="config")
    print(f"Bot was removed from {guild.name} (Guild ID: {str(guild.id)})")

#msgcount = discord.SlashCommandGroup(name="msgcount", description="Command group for the message count feature")
msgcount = bot.create_group("msgcount", "Command group for the message count feature")
#----------
@msgcount.command(description = "What's the message count feature works and how to set it up")
async def guide(ctx: discord.ApplicationContext):
    await ctx.respond(  "## About the message count feature\n"
                        "The message count feature is a feature that counts how many messages a user has sent in the server. It's a simple feature that can be useful for some servers.\n"
                        "You are limited to track maximum of 10 users. This feature will also be off by default and need configuration.\n"
                        "## How to set it up\n"
                        "You could use the `/msgcount toggle` command to toggle the feature. The slash command requires inputs of users you want to track (10 maximum).\n"
                        "The bot will start tracking then\n"
                        "## Commands:\n"
                            "- `/msgcount config` - Configure the message count feature, requires Administrator permission\n"
                                "- `/msgcount config toggle` - Toggle the message count feature (off by default)\n"
                                "- `/msgcount config view` - View the configuration of the message count feature\n"
                                "- `/msgcount config add` - Add user(s) to track list\n"
                                "- `/msgcount config write` - Rewrite the track list\n"
                                "- `/msgcount config remove` - Remove user(s) from track list\n"
                            "- `/msgcount get` - See how many messages members sent, requires Mention Everyone permission\n"
                            "- `/msgcount delete` - Delete the message count data of your server, requires Administrator permission\n"
                      )
#----------
msgcount_config = msgcount.create_subgroup(name="config", description="Configure the message count feature", guild_only=True, default_member_permissions= discord.Permissions(administrator=True))
@msgcount_config.command(description = "Configure the message count feature",
                         contexts={discord.InteractionContextType.guild},)
@discord.default_permissions(
    administrator = True
)
async def toggle(ctx: discord.ApplicationContext):
    if get_data(server_id=str(ctx.guild_id), collection="config") is None or get_data(server_id=str(ctx.guild_id), collection="config")["msgcount"]["toggle"] == "false":
        update_db_one(server_id=str(ctx.guild_id), collection="config", bkeys="msgcount", toggle="true")
        await ctx.respond("Message count feature is now on. Do `/msgcount config toggle` again to turn off.")
    elif get_data(server_id=str(ctx.guild_id), collection="config")["msgcount"]["toggle"] == "true":
        update_db_one(server_id=str(ctx.guild_id), collection="config", bkeys="msgcount", toggle="false")
        await ctx.respond("Message count feature is now off. Do `/msgcount config toggle` again to turn on.")
#
@msgcount_config.command(description = "View the configuration of the message count feature",
                         contexts={discord.InteractionContextType.guild},)
@discord.default_permissions(
    administrator = True,
    mention_everyone = True,
)
async def view(ctx: discord.ApplicationContext):
    output = f"Toggle: {get_data(server_id=str(ctx.guild_id), collection='config')['msgcount']['toggle']}\n"
    output = ("Tracked users: ")
    if get_data(server_id=str(ctx.guild_id), collection="message_count")["msgcount"]["list"] is not None:
        users = get_data(server_id=str(ctx.guild_id), collection="message_count")["msgcount"]["list"]
        for user in users:
            output += f"<@{user}>, "
        output = output[0:-2]
    elif get_data(server_id=str(ctx.guild_id), collection="message_count")["msgcount"]["list"] is None:
        output += "`No users tracked`"
#
@msgcount_config.command(description = "Add user(s) to track list",
                         contexts={discord.InteractionContextType.guild},)
@discord.default_permissions(
    administrator = True
)
async def add(ctx: discord.ApplicationContext, user: list[discord.User]):
    users = get_data(server_id=str(ctx.guild_id), collection="message_count")["msgcount"]["list"]
    users += user
    update_db_one(server_id=str(ctx.guild_id), collection="message_count", bkeys="msgcount.list", method="set", user_id=str(ctx.author.id), users=users)
#
@msgcount_config.command(description = "Rewrite the track list",
                        contexts={discord.InteractionContextType.guild},)
@discord.default_permissions(
    administrator = True
)
async def write(ctx: discord.ApplicationContext, user: list[discord.User]):
    update_db_one(server_id=str(ctx.guild_id), collection="message_count", bkeys="msgcount.list", method="set", user_id=str(ctx.author.id), users=user)
#
@msgcount_config.command(description = "Remove user(s) from track list",
                         contexts={discord.InteractionContextType.guild},)
@discord.default_permissions(
    administrator = True
)
async def remove(ctx: discord.ApplicationContext, user: list[discord.User]):
    users = get_data(server_id=str(ctx.guild_id), collection="message_count")["msgcount"]["list"]
    for u in user:
        try:
            users.remove(u)
        except ValueError:
            continue

#----------
@msgcount.command(description = "See how many messages members sent",
                  contexts={discord.InteractionContextType.guild},)
@discord.default_permissions(
    mention_everyone = True,
)
async def get(ctx: discord.ApplicationContext):
    if str(ctx.guild_id) == "1303613693707288617":
        data = get_data(server_id=str(ctx.guild_id), collection="message_count")
        response = ""
        try:
            for user_id, count in data.items():
                if user_id == "_id":
                    continue
                response += f"> <@{user_id}> Sent `{count}` messages\n"
            response.strip()
            await ctx.respond(response)
        except AttributeError:
            await ctx.respond("No data found.")
        else:
            raise UnknownError
    else:
        await ctx.respond("This feature is not available for everyone yet.")
#----------
@msgcount.command(description = "Delete the message count data of your server",
                  contexts={discord.InteractionContextType.guild},
)
@discord.default_permissions(
    administrator = True,
)
async def delete(ctx: discord.ApplicationContext):
    write_to_db_one(server_id=str(ctx.guild_id), collection="message_count", confirm = str(ctx.author.id))
    await ctx.respond(f"Dm <@{str(bot.user.id)}> : `/msgcount confirm_deletion {str(ctx.guild_id)}` to confirm the deletion\nor `/msgcount cancel_deletion {str(ctx.guild_id)}` to cancel the deletion")
#----------
@msgcount.command(description = "Confirm the deletion of the message count data of your server",
                  contexts={discord.InteractionContextType.bot_dm},
)
@discord.option(
    "server_id",
    description="The server ID",
    required=True,
)
async def confirm_deletion(ctx: discord.ApplicationContext, server_id: int):
    if str(ctx.author.id) == get_data(server_id=str(server_id), collection="message_count")["confirm"]:
        delete_data_one(server_id=str(server_id), collection="message_count")
        await ctx.respond("Data deleted")
    else:
        await ctx.respond("You are not authorized to delete the data. If you have permission, try doing `/msgcount delete` in your server.")
#----------
@msgcount.command(description = "Cancel the deletion of the message count data of your server",
                  contexts={discord.InteractionContextType.bot_dm},
)
@discord.option(
    "server_id",
    description="The server ID",
    required=True,
)
async def cancel_deletion(ctx: discord.ApplicationContext, server_id: int):
    if str(ctx.author.id) == get_data(server_id=str(server_id), collection="message_count")["confirm"]:
        update_db_one(server_id=str(server_id), collection="message_count", confirm = "0")
        await ctx.respond("Deletion canceled")
    else:
        await ctx.respond("You are not authorized to cancel the deletion. If you have permission, try doing `/msgcount delete` in your server.")
#===============================================

#=================================================================================================================================

def main():
    #bot.add_application_command(msgcount)
    bot.run(TOKEN)

if __name__ == '__main__':
    main()  