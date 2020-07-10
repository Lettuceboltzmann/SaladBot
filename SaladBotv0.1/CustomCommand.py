#File to hold class to build and store custom commands

import discord
from pathlib import Path

class CustomCommand:
    def __init__(self, bot, GUILD):

        #There will be some reworking of the code to utilize these object properties
        guild = discord.utils.get(bot.guilds, name=GUILD)
        self.CommandName = ''
        self.CommandResponse = ''
        self.CommandDescription = ''
        
        commandFolder = Path(guild.name).mkdir(parents=True, exist_ok=True)
        self.commandFile = guild.name + '/' + guild.name + '.comms'
            

    #Creates New Command
    def CreateCommand(commandFile, commandList, newCommandName, newCommandResponse):
        with open(commandFile, "a") as f:
            f.write("!" + newCommandName + ';' + newCommandResponse + "\n")
        commandList.clear()
        CustomCommand.LoadCommands(commandFile, commandList)
        print(f"Command: !{newCommandName} added.\n")

    #Loads all custom commands from file.
    def LoadCommands(commandFile, commandList):
        print(f'Loading custom commands from: {commandFile}\n')
        with open(commandFile) as f:
            for line in f:
                (key, val) = line.split(';')
                commandList[key] = val
        return commandList

    def RemoveCommand(commandFile, commandList, oldCommandName, oldCommandResp):
        with open(commandFile, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if line != (oldCommandName + ";" + oldCommandResp):
                    f.write(line)
            f.truncate()
            commandList.clear()
            CustomCommand.LoadCommands(commandFile, commandList)
        print(f"Removed {oldCommandName}.\n")

    def EditCommand(commandFile, commandList, oldCommandName, oldCommandResp, newResponse):
        with open(commandFile, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if line != (oldCommandName + ";" + oldCommandResp):
                    f.write(line)
            f.write(oldCommandName + ";" + newResponse + "\n")
            f.truncate()
            commandList.clear()
            CustomCommand.LoadCommands(commandFile, commandList)
        print(f"{oldCommandName} edited successfully.\n")
