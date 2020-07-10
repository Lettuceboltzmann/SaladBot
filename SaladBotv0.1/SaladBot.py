#SaladBot v0.1
#By LettuceBoltzmann
#Contact: lettuce.boltzmann@gmail.com

import os
import csv
import random
import discord
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands

#Custom classes
from CustomCommand import CustomCommand

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="?")

#List to contain all custom commands
global localCommands    #This is a global variable for the sake of not being able to pass to on_ready()
localCommands = {} 

#Timer for bot uptime
uptimeTime = datetime.now()

@bot.event
#Custom commands will be loaded on connection.
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
            f"{bot.user.name} is connected to Discord!\n"
            f"{bot.user.name} is connected to the following server(s):\n"
            f"{guild.name}(id: {guild.id} at {uptimeTime}."
    )
    LoadCommands = CustomCommand(bot, GUILD)
    global localCommands
    localCommands = CustomCommand.LoadCommands(LoadCommands.commandFile, localCommands)

#Custom command calls
@bot.event
async def on_message(message):
    global localCommands
    if message.author == bot.user:
        return
    for key in localCommands:
        if key == message.content.lower():
            await message.channel.send(localCommands[key])
    await bot.process_commands(message)

#Rolls dice based on user input
@bot.command(
        name='dice', 
        help="Rolls dice. Command structure: ?dice <# dice> <# sides>. " 
            "With no argument, will just roll one 6-sided die."
)
async def roll(ctx, number_of_dice: int = 1, number_of_sides: int = 6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

#Lists bot uptime
@bot.command(
        name = "uptime",
        help = "Gets bot uptime of current session."
)
async def uptime(ctx):
    #There's probably a much better way to handle this. I'll deal with this later.
    timeDifference = datetime.now() - uptimeTime
    hours = (timeDifference.days * 24 % 24) + timeDifference.seconds // 3600
    minutes = timeDifference.seconds % 3600 // 60
    seconds = timeDifference.seconds % 60
    if (timeDifference.days == 0 and hours == 0 and minutes == 0):
        response = "SaladBot has been online for " + str(seconds) + " seconds."
    elif (timeDifference.days == 0 and hours == 0):
        response = "SaladBot has been online for " + str(minutes) + " minutes, " + str(seconds) + " seconds."
    elif (timeDifference.days == 0):
        response = "SaladBot has been online for " + str(hours) + " hours, " + str(minutes) + " minutes, " + str(seconds) + " seconds."
    else:
        response = "SaladBot has been online for " + str(timeDifference.days) + " days, " + str(hours) + " hours, " + str(minutes) + " minutes, " + str(seconds) + " seconds."
    await ctx.send(response)

#Create Custom Command
@bot.command(name="newcommand", help="Adds custom command.")
@commands.has_role('admin')
async def newcommand(ctx, newcmd = '', newresp = ''):
    if newcmd == '' or newresp == '':
        response = "Error adding command! Use: \'/newcommand <command name> <command response>\'"
        await ctx.send(response)
        return
    global localCommands
    NewCommand = CustomCommand(bot, GUILD)
    CustomCommand.CreateCommand(NewCommand.commandFile, localCommands, newcmd, newresp)
    response = "New command: !" + newcmd + " added."
    await ctx.send(response)

#Remove custom command
@bot.command(name="removecommand", help="Removes custom command.")
@commands.has_role('admin')
async def removecommand(ctx, oldcmd = ''):
    if oldcmd == '':
        response = "No command to remove. Use: \'/removecommand <command name>\'"
        await ctx.send(response)
        return
    global localCommands
    oldcmd = "!" + oldcmd
    oldresp = localCommands[oldcmd]
    if oldcmd in localCommands:
        RemoveCommand = CustomCommand(bot, GUILD)
        CustomCommand.RemoveCommand(RemoveCommand.commandFile, localCommands, oldcmd, oldresp)
        response = oldcmd + " removed."
        await ctx.send(response)
    else:
        response = "No command \'" + oldcmd + "\' to remove."

#Edit custom command

@bot.command(name="editcommand", help="Edits existing custom command.")
@commands.has_role("admin")
async def editcommand(ctx, oldcmd = '', newresp = ''):
    if oldcmd == '':
        response = "No input. Use: <command name> <new command response>"
        await ctx.send(response)
        return
    global localCommands
    oldcmd = "!" + oldcmd
    oldresp = localCommands[oldcmd]
    if oldcmd in localCommands:
        EditCommand = CustomCommand(bot, GUILD)
        CustomCommand.EditCommand(EditCommand.commandFile, localCommands, oldcmd, oldresp, newresp)
        response = "Command " + oldcmd + " edited successfully."
        await ctx.send(response)
    else:
        response = "Command " + oldcmd + " not found. Please Try again."
        await ctx.send(response)
        return

#List all custom commands
@bot.command(name="commands", help="Lists all custom commands.")
async def commands(ctx):
    global localCommands
    response = "Custom commands:\n"
    for key in localCommands:
        response += key + "\n"
    await ctx.send(response)

bot.run(TOKEN)
