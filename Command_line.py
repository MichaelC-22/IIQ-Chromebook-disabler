import commandSayings as CS
import os
import savethingstofile as SF
import error_checker as ec
import logging as log
import datetime
SNfile= "SerialNumbers.txt"

class commandLine:
    # gets the current date
    currentTime = datetime.datetime.now()
    # creates a file with the current date as the file name in the log file
    log.basicConfig(level=log.INFO,
                 format= "%(asctime)s ** %(levelname)s ** %(message)s",
                 datefmt= "%Y/%m/%d %H:%m",style= "%",
                 filename= "logs/" + currentTime.strftime("%Y-%m-%d") + ".log",
                 filemode= "a",
                 encoding= "utf-8"
                )
    
    #logs that commandLine was loaded
    log.info("loaded commandLine")

    def startUpCommandLine(self):
        # logs that this function ran
        log.info("Running startUpComamndLine in commandLine")
        # checks to see if the user has run the program before
        if(os.path.exists("userinfo.txt") == False):
            # prints the first time welcome message
            CS.commandSayings.firstWelcome(CS.commandSayings())
            # creates a file
            f = open("userinfo.txt", "x")
            # closes the file
            f.close()
            # walks the user though the set up process for this app
            CS.commandSayings.startupProcess(CS.commandSayings())
            # continues
            pass
        else:
            # prints the basic message
            CS.commandSayings.basicWelcome(CS.commandSayings())
            CS.Command_line.commandLine.commandLine(CS.Command_line.commandLine())

    def commandLine(self):
        # logs that this function ran
        log.info("Running commandLine in commandLine")
        # files used in the program
        IIQ = "IIQ_info.txt"
        userInfo = "userinfo.txt"
        
        try:
            # keeps the app running
            running = True
            while(running):
                # gets user input
                user = input("Command: ")
                user = user.strip()
                # checks to see what the user entered
                if (user == "-help" or user == "-h"):
                    # prints the help page
                    CS.commandSayings.help(CS.commandSayings())
                elif(user == "-quit" or user == "-Quit" or user == "-q"):
                    # closes the program
                    running = False
                    return running
                elif(user == "change IIQ info" or user == "Change IIQ info"):
                    # checks if the file IQInfo exists
                    if(os.path.exists(IIQ)):
                        # Creates the file and saves the data to it
                        try:
                            # gets the users input
                            APIToken = input("Enter the IQ API token: ")
                            API_url = input("Enter the IQ API url: ")
                            disabledID = input("Enter the disabled ID: ")
                            productID = input("Enter the product ID: ")
                            # saves the users input
                            SF.saveThingToFiles.saveToFile(SF.saveThingToFiles(), IIQ, APIToken, "")
                            SF.saveThingToFiles.saveToFile(SF.saveThingToFiles(), IIQ, API_url, "")
                            SF.saveThingToFiles.saveToFile(SF.saveThingToFiles(), IIQ, disabledID, "")
                            SF.saveThingToFiles.saveToFile(SF.saveThingToFiles(), IIQ, productID, "")
                        except:
                            # logs that the command was canceled
                            log.warning("Canceling command")
                            # tells the user the command was canceled
                            print("\nCanceling command")
                    # clears the existing file and adds the info to it
                    else:
                        # Deletes the file
                        SF.saveThingToFiles.clearFile(SF.saveThingToFiles(), IIQ)
                        # creates the file
                        try:
                            # gets the user input
                            APIToken = input("Enter the IQ API token: ")
                            API_url = input("Enter the IQ API url: ")
                            disabledID = input("Enter the disabled ID: ")
                            productID = input("Enter the product ID: ")
                            # saves the user input
                            SF.saveThingToFiles.saveToFile(SF.saveThingToFiles(), IIQ, APIToken, "")
                            SF.saveThingToFiles.saveToFile(SF.saveThingToFiles(), IIQ, API_url, "")
                            SF.saveThingToFiles.saveToFile(SF.saveThingToFiles(), IIQ, disabledID, "")
                            SF.saveThingToFiles.saveToFile(SF.saveThingToFiles(), IIQ, productID, "")
                        except:
                            # logs that the command was canceled
                            log.warning("Canceling command")
                            # tells the user the command was canceled
                            print("\nCanceling command")
                # allows the user to set the time for chromebooks to be disabled
                elif(user == "set time" or user == "Set time"):
                    try:
                        # used to allow the user to miss enter a word and not mess up teh program
                        inDisableEveryDay:bool = True
                        while(inDisableEveryDay):
                        # ask the user if they want to disable the chromebooks every day
                            user = input("Do you want the chromebooks to be disabled at the end of every day?\n")
                            if(user == "yes" or user == "Yes" or user == "y"):
                                disableEveryday:bool = True
                                inDisableEveryDay:bool = False
                            elif(user == "no" or user == "No" or user == "n"):
                                disableEveryday:bool = False
                                inDisableEveryDay:bool = False
                            else:
                                print("Enter yes or no")
                        # ask the user for the hour to disable the chromebooks everyday at
                        if(disableEveryday == True): # type: ignore
                            inDisableEveryDay = True
                            while(inDisableEveryDay):
                                userTime = input("Enter the hour you want the chromebooks to be disabled by.\nDont forget to use AM or PM if your not using military time.\n")
                                if(ec.error_checker.isTimeCorrect(ec.error_checker(), userTime)):
                                        inDisableEveryDay = False
                        else:
                        # ask the user for a custom time to disable the chromebooks. example every 2 days after they have been checked out
                            inCustomDay = True
                            while(inCustomDay):
                                userTime = input("Enter how many days you want to pass between disabling sessions.\n")
                                if(ec.error_checker.isTimeCorrect(ec.error_checker(), userTime)):
                                    inCustomDay = False
                        # ask the user if they want to use a custom hour to disable the chromebooks. The default is 12 AM
                            specific_time = input("The defult hour a chromebook will be disabled after " + userTime + " days is 12AM.\n Do you want to change that?\n") # type: ignore
                        # allows the user to mess up spelling without breaking the program
                            inSpecificTime = True
                            while(inSpecificTime):
                                specific_time = input("Enter the hour you want the chromebook to be disabled.\nUse AM or PM if your not using military time\n")
                                # Set the specific hour they want them disabled by.
                                if(specific_time == "Yes" or specific_time == "yes" or specific_time == "y"):
                                    if(ec.error_checker.isTimeCorrect(ec.error_checker(), specific_time)):
                                        inSpecificTime = False
                                # Sets the hour to the default of 12 AM
                                elif(specific_time == "No" or specific_time == "no" or specific_time == "n"):
                                    specific_time = "12 AM"
                                    inSpecificTime = False
                                else:
                                    print("Enter yes or no")
                    except Exception:
                        # logs the unknown error
                        log.critical("Unknown error: ", exc_info=True)
                    # formats the days need to pass correctly
                    userTime = "Days needed to pass: " + userTime + "," # type: ignore
                    # formats the specific hour correctly
                    specific_time = "Specific hour: " + specific_time + "," # type: ignore
                    # Changes the user's time
                    try:
                        SF.saveThingToFiles.changeLineInFile(SF.saveThingToFiles(), userInfo, userTime, "Days needed to pass: ")
                        SF.saveThingToFiles.changeLineInFile(SF.saveThingToFiles(), userInfo, specific_time, "Specific hour: ")
                    except TypeError:
                        # logs the type error
                        log.warning("there was a type error")
                        SF.saveThingToFiles.saveToFile(SF.saveThingToFiles(), userInfo, userTime, "")
                        SF.saveThingToFiles.saveToFile(SF.saveThingToFiles(), userInfo, specific_time, "")
                    except Exception:
                        # logs the unknown error
                        log.critical("Unknown error: ", exc_info=True)
                # allows the user to add Serial numbers to the program
                elif (user == "add SN"or user == "Add SN"):
                    # tells the user how to add teh serial numbers
                    print("\nWhen adding Serial numbers please seperate the serial numbers with just a space.\n")
                    print("One you have entered all the serial numbers click enter")
                    print("Example: SN1 SN2 SN3...\n")
                    # gets teh serial numbers from the user
                    sn = input("Serial Numbers: ")
                    try:
                        # creates the SerialNumber file
                        with open("SerialNumbers.txt", "x") as file:
                            #replaces every space with the new line character
                            sn = sn.replace(" ", "\n")
                            # writes the new string to the file
                            file.write(sn)
                        # closes the file
                        file.close()
                    except FileExistsError:
                        # logs the file exists
                        log.info("The file exists")
                        # adds the serial numbers to the file
                        with open("SerialNumbers.txt", "a") as file:
                            # replaces all spaces with a new line character
                            sn = sn.replace(" ", "\n")
                            file.write("\n")
                            # writes the new string to the file
                            file.write(sn)
                        # closes the file
                        file.close()
                    except Exception:
                        # logs the unknow error
                        log.critical("Unknown error: ", exc_info=True)
                # allows the user to remove either all the serial numbers or a specific serial number       
                elif(user == "remove SN" or user== "Remove SN"):
                    # tells the user how to remove all the serial numbers
                    print("\nTo remove all serial numbers type all.\n")
                    # tells the user howto remove a specific serial number
                    print("To remove a specific serial number type that serial number.\n")
                    # gets the serial numbers
                    sn = input("Serial Numbers: ")
                    if(sn == "All" or sn == "all"):
                        # removes the SerialNumbers.txt file
                        os.remove("SerialNumbers.txt")
                        # tells the user the serial numbers has been removed
                        print("Serial numbers have been removed.\n")
                    else:
                        with open("SerialNumbers.txt", "r") as f:
                            #creates a list that contaions all the serial numbers
                            lines = f.readlines()
                        with open("SerialNumbers.txt", "w") as f:
                            for line in lines:
                                # check to see if line does not equal the SN
                                if line.strip("\n") != sn.strip("\n"):
                                    # writes line to the file
                                    f.write(line)
                else:
                    print("\nThat is not a valid command. If you need help type -h.\n")
        except KeyboardInterrupt:
            # logs the start of the disabling process
            log.info("starting disabling process")
            # tells the user the disabling process started
            print("\n\nstarting disabling process.\n")