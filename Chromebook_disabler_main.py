import datetime
import os
import Command_line as cl
import incidentIQ as IQ
import stringSufer as SS
import threading as th
import time
import signal
import logging as log


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
    
#logs that commandLine was loaded
log.info("loaded main")
# the files that should be created for the program to run
SNfile= "SerialNumbers.txt"

userFile = "userinfo.txt"

IQFile = "IIQ_info.txt"

# disables the chromebooks after a certen number of days
def daysDisabler(days: int, minutes: int):
    # logs that this function ran
    log.info("Running daysDisabler in Chromebook_disabler_main")
    # sets day counter to 0
    dayCounter = 0
    # adds the commandline to a threading task
    commandline = th.Thread(target = cl.commandLine.startUpCommandLine(cl.commandLine()))
    # starts the threading task
    commandline.start()
    runningBigLoop = True
    while(runningBigLoop):
        if(dayCounter == days):
            # resets the day counter
            dayCounter = 0
            # stars the second while loop
            runningSmallLoop = True
            # runs until the current time equals the user's time
            while(runningSmallLoop):
                # gets the current time
                currentTime = datetime.datetime.now()
                # converts the current time to minutes
                currentTime = (currentTime.hour * 60) + currentTime.minute
                # checks if the current time equals the user's time
                if(currentTime == minutes):
                    # kills the command line
                    os.kill(os.getpid(), signal.SIGINT)
                    #closes the commandline thread
                    commandline.join()
                    file = SNfile
                    # starts a thread for disableTheChromebooks and passess in the SNfile
                    disabler = th.Thread(target=IQ.incidentIQ.disableTheChromebooks, args=[IQ.incidentIQ(), file])
                    # starts the thread
                    disabler.start()
                    # waits for the thread to finish the closes it properly
                    disabler.join()
                    # waits 2 minutes before going back into the while loop
                    time.sleep(120)
                    # stops the second while loop
                    runningSmallLoop = False
                    runningBigLoop = False
                # waits a minute
                time.sleep(60)
        # waits a day
        time.sleep((24 * 60 * 60))
        # increases the day counter
        dayCounter = dayCounter + 1

# disables the chomebooks once the current time is the user's entered time 
def everyDayDisabler(minutes: int):
    # logs that this function ran
    log.info("Running everyDayDisabler in Chromebook_disabler_main")
    # gets the current time
    currentTime = datetime.datetime.now()
    # converts the current time to minutes
    currentTime = (currentTime.hour * 60) + currentTime.minute
    while(currentTime != minutes):
        # gets the current time
        currentTime = datetime.datetime.now()
        # converts the current time to minutes
        currentTime = (currentTime.hour * 60) + currentTime.minute
        # checks if the current time equals the user's time
        if(currentTime == minutes):
            # kills the command line
            os.kill(os.getpid(), signal.SIGINT)
            # starts a thread for disableTheChromebooks and passess in the SNfile
            files = SNfile
            disabler = th.Thread(target=IQ.incidentIQ.disableTheChromebooks, args=[IQ.incidentIQ(), files])
            # starts the thread
            disabler.start()
            # waits for the thread to finish the closes it properly
            disabler.join()
            # waits 2 minutes before going back into the while loop
            time.sleep(90)
        # waits a minute before checking the time again
        time.sleep(60)
        
        

def main():
    # logs that this function ran
    log.info("Running main in Chromebook_disabler_main")
    
    # used to see if certain files exist
    UserFileExists = False
    SNFileExists = False
    IQFileExists = False
    running = True
    
    try:
        if __name__ == "__main__":
            # clears the screen
            os.system("clear")
            # checks if the user file exists
            if (os.path.exists(userFile)):
                UserFileExists = True
            # checks if the serial number file exists
            if(os.path.exists(SNfile)):
                SNFileExists = True
            # checks if the Incident IQ file exists
            if(os.path.exists(IQFile)):
                IQFileExists = True
            # runs if all the files and directorys needed exists
            if(IQFileExists and SNFileExists and UserFileExists):
                while(running):
                    # gets disable every day from the userinfo.txt
                    disableEveryDayFromFile:str = SS.stringSurfer.removeStringFromline(SS.stringSurfer(), userFile, "Daily check: ", 2)
                    disableEveryDayFromFile = str(disableEveryDayFromFile).strip()
                    # checks if disableEveryDay is fasle
                    if(disableEveryDayFromFile == "False" or disableEveryDayFromFile == "false"):
                        # sets disableEveryDay to false
                        disableEveryDay = False
                    # checks if disableEveryDay is true
                    elif(disableEveryDayFromFile == "True" or disableEveryDayFromFile == "true"):
                        # sets disableEveryDay to true
                        disableEveryDay = True
                    # if disableEveryDay is something other then true or false
                    else:
                        # sets disableEveryDay to false
                        disableEveryDay = False
                    # converts the time the user entered into minutes
                    disableTime = IQ.incidentIQ.convertToMinutes(IQ.incidentIQ())
                    # gets the number of days the user entered
                    disableDay = SS.stringSurfer.removeStringFromline(SS.stringSurfer(), userFile, "Days needed to pass: ", 1)
                    disableDay = int(disableDay)
                    # checks if the user wants to disable the chromebooks everyday
                    if(disableEveryDay):
                        info = [disableTime]
                        # makes a thread for the everyDayDisabler funtion
                        everydayDisabling = th.Thread(target=everyDayDisabler, args=info)
                        # starts the everyDayDisabler funtion
                        everydayDisabling.start()
                        # adds the commandline to a threading task
                        commandline = th.Thread(target = cl.commandLine.startUpCommandLine(cl.commandLine()))
                        # starts the threading task
                        commandline.start()
                        # checks if everydayDisabler is running
                        while(everydayDisabling.is_alive() == True):
                            # waits a minute
                            time.sleep(60)
                        #closes the commandline thread
                        commandline.join()
                    # runs if they dont
                    else:
                        info = [disableTime, disableDay]
                        # makes a thread for the day disabler
                        daydisabling = th.Thread(target=daysDisabler, args=info)
                        # starts the day disabler
                        daydisabling.start()
                        # adds the commandline to a threading task
                        commandline = th.Thread(target = cl.commandLine.startUpCommandLine(cl.commandLine()))
                        # starts the threading task
                        commandline.start()
                        # checks if the daydisabler is running
                        while(daydisabling.is_alive() == True):
                            # waits a minute
                            time.sleep(60)
                        #closes the commandline thread
                        commandline.join()

            else:
                try:
                    # if all the files do not exist it is the user's first time running the program. the program then runs the basic start up processes
                    if(SNFileExists == False and IQFileExists == False and UserFileExists == False):
                        # adds the commandline to a threading task
                        thread3 = th.Thread(cl.commandLine.startUpCommandLine(cl.commandLine()))
                        # starts the threading task
                        thread3.start()
                    else:
                        # tells the user they are missing the serial number file and tells the how to add it.
                        if(SNFileExists == False):
                            # tells the user what file they are missing
                            print("You are missing the file that contains the serial numbers of the computers.\n\nType GUI then add the serial numbers.\n")
                        # tells the user that they are missing the incident IQ file and how to add it
                        if(IQFileExists == False):
                            # tells the user what file they are missing
                            print("You are missing the file that contains the incident IQ infomation.\n\nType GUI then click Change IQ info to add the infomation.\n")
                        # tells the user that they are missing the user file and how to add it
                        if(UserFileExists == False):
                            # tells the user what file they are missing
                            print("You are missing the file that contains when the computers should be disabled.\n\nType GUI then click set time to add this information.\n")
                        # adds the commandline to a threading task
                        thread3 = th.Thread(target=cl.commandLine.commandLine(cl.commandLine())) # type: ignore
                        # starts the threading tasks
                        thread3.start()  
                # For unexpected errors
                except Exception:
                    # logs the unknown error
                    log.critical("Unknown error: ", exc_info=True)
    # for unexpected errors
    except Exception:
        # logs the unknown error
        log.critical("Unknown error: ", exc_info=True)      
# runs the main file
main()