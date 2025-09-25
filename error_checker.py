import logging as log
import datetime

class error_checker:
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
    #logs that error_checker loaded
    log.info("loaded error_checker")
    
    # checks if what the user entered was an whole number     
    def isInt(self, user:str):
        # logs that this function ran
        log.info("Running isInt in error_checker")
        try:
            # checks if user is a whole number
            if(int(user)):
                 return True
            else:
                # causes an Valueerror
                 int(user)
        # tells the user to enter a number
        except ValueError:
            # logs that the value entered was not a number
            log.warning("The value that was entered was not a number")
            print("enter a number")
            return False
        # For unexpected errors
        except Exception:
                log.critical("Unknow error: ", exc_info=True)

    # checks if the time the user entered is the correct formate
    def isTimeCorrect(self, user:str):
        # logs that this function ran
        log.info("Running isTimeCorrect in error_checker")
        try:
            # checks if user contains am
            if(str(user).lower().find("AM")):
                # removes am
                time = str(user).lower().removesuffix("am").strip()
                # checks if the time is a number
                if(error_checker.isInt(self, time)):
                    return True
            # Checks if user conatins pm
            elif(str(user).lower().find("PM")):
                # removes pm from user
                time = str(user).lower().removeprefix("pm").strip()
                # checks if time is a number
                if(error_checker.isInt(self, time)):
                    return True
            # checks if user contains :
            elif(str(user).find(":")):
                isCorrect = 0
                # removers everything after the :
                time = str(user)[:str(user).find(":")] + ""
                # checks if time is a number
                if(error_checker.isInt(self, time)):
                    # adds one to the correct counter
                    isCorrect = isCorrect + 1
                # removes everything before the :
                time = str(user)[str(user).find(":"):] + ""
                # checks if time is a number
                if(error_checker.isInt(self,user)):
                    # adds one to the correct counter
                    isCorrect = isCorrect + 1
                # Checks if isCorrect equals 2
                if(isCorrect == 2):
                    # returns True
                    return True
        # lets the user know they entered the time wrong and how it is suppost to be
        except ValueError:
            #logs that the value entered was not correct
            log.warning("Value enterd was not correctly formated as time")
            # tells the user that the entered time was not correctly formated
            print("The time was entered incorrectly.\nYou entered " + str(user) + ".\nPlease entered the time either in am or pm or in military time.\nFor example, 12 AM or 12:00")
            return False
        # For unexpected errors
        except Exception:
            # logs the unknow error
            log.critical("Unknow error: ", exc_info=True)
    
    

                 