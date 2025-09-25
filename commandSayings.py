import os
import Command_line
import logging as log
import datetime

class commandSayings:
    # gets the current date
    currentTime = datetime.datetime.now()
    # creates a file with the current date as the file name in the log file
    log.basicConfig(level=log.INFO,
                 format= "%(asctime)s ** %(levelname)s ** %(message)s",
                 datefmt= "%Y/%m/%d %H:%M",
                 style= "%",
                 filename= "logs/" + currentTime.strftime("%Y-%m-%d") + ".log",
                 filemode= "a",
                 encoding= "utf-8"
                )
    
    #logs that commandSaying was loaded
    log.info("loaded commandSaying")
    
    # Tells the user a bit about the program
    def firstWelcome(self):
        # logs that this function ran
        log.info("Running firstWelcome in commandSaying")
        # clears the terminal
        os.system("clear")
        # welcomes the user to the program and tells the user a bit about the program
        print("Welcome to the loaner chromebook disabler\n")
        print("\t‣ This program allows you to enter serial numbers of chromebooks to be automaticly disabled after a certian amount of time has passed.\n")
        print("\t‣ This program sets the Chromebook's status in IncidentIQ and Google admin to disabled\n")
        print("Now lets get started!\n")
        
    # helps the user set up the program
    def startupProcess(self):
        # logs that this function ran
        log.info("Running startupProcess in commandSaying")
        # Tells the user how to change the IIQ info
        print("\n\nThe first thing you need to do is enter your company's IIQ info\n")
        print("To do this type Change IIQ info\n")
        print("Then follow the prompts\n")
        print("Once you are done type quit\n\n")
        # opens the commandline
        Command_line.commandLine.commandLine(Command_line.commandLine())
        # tells the user how to select the time to disable the chromebooks
        print("Next you have to set the time you want the chomebookes to get disabled\n")
        print("To do this type set time\n")
        print("Then follow the prompts\n")
        print("Once you are done type quit\n\n")
        # opens the commandline
        Command_line.commandLine.commandLine(Command_line.commandLine())
        # tells the user how to add serial numbers
        print("Now the last thing you need to do is enter the serial numbers of the Chromebooks.\n")
        print("You can do this by either typing add SN or by creating a .txt file named exactly 'SerialNumbers.txt'.\n")
        print("Which way would you like to create the file. (command or file)\n\n")
        # gets the way the user wants to add serial numbers
        user = input("Command: ")
        if (user == "command" or user == "Command"):
            # tells the user how to add Seiral number using the command line
            print("\n\nType add SN.\n")
            print("Then follow the prompts\n")
            print("Once you are done type quit\n\n")
            Command_line.commandLine.commandLine(Command_line.commandLine())
        elif(user == "file" or user == "File"):
            # tells the user how to add seiral numbers by puting a file into the folder of the program
            print("As stated before the serial number file must be named exactly 'SerialNumbers.txt'.\n")
            print("It can not include commas and each serial number should be on a different line.\n")
            print("One you have created the file and moved it into the folder which contains this program you are all set to go.\n")
        # tells the user the program is now open it's command line
        print("Now opening the command line.\n")
        print("Remember if you need help type -h\n\n")
        Command_line.commandLine.commandLine(Command_line.commandLine())

    # welcomes the user back to the program
    def basicWelcome(self):
        # logs that this function ran
        log.info("Running basicWelcome in commandSaying")
        # clears the terminal
        os.system("clear")
        # welcomes the user back to the program
        print("Welcome back\n")
        print("If you need help type -help or -h\n")
        
    # the help page
    def help(self):
        # logs that this function ran
        log.info("Running help in commandSaying")
        # tells the users the commands they can do
        print("\n-help: shows this help page.\n")
        print("-quit: closes the program\n")
        print("change IQ info: allows you to change the site, API_Token, API_url, etc. for Incident IQ.\n")
        print("set time: allows you to set the time intervals of which the disability accurse.\n")
        print("add SN: allows you to add serial numbers to the SerialNumber file.\n")
        print("remove SN: Allows you to remove a serial number or all serial numbers.\n")