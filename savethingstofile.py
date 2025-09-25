import os
import io
import logging as log
import datetime

class saveThingToFiles:
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

    # logs that stringSufer was loaded
    log.info("Loaded saveThingToFiles")
    
    # Either creates the save file or adds to it
    def saveSNToFile(self, file: str, sn: str):
        # logs that this function ran
        log.info("Running saveSNToFile in saveThingToFiles")
        # checks to see if the file has any commas
        sn = sn.upper()
        if(sn.find(",")):
            # will try appending the entered serial numbers
            try:
                # opens the entered file as appending
                with open(file, "a") as snfile:
                    # creates a list of every entered serial number
                    snList:list[str] = sn.split(",")
                    # goes through the list
                    for x in sn: #type: str
                        i = 0
                        # appends the serial number to the file then goes to a new line
                        snfile.write(snList[i] + "\n")
                        i = i + 1
                    # close the file
            except FileExistsError:
                # logs that the file was not found
                log.warning("File not found")
                # creates the file
                with open(file, "x") as snfile:
                    # creates a list of every entered serial number
                    snList = sn.split(",")
                    # goes though the list
                    for x in sn: #type: str
                        i = 0
                        # appends the serial number to the file then goes to a new line
                        snfile.write(snList[i] + "\n")
                        i = i + 1
            except Exception as e:
                # logs the unknow error
                log.critical("Unknow error: ", exc_info=True)
        else:
            # runs if only one serial number is enterd
            try:
                # opens the file as appending
                with open(file, "a") as snfile:
                    # appends the serial number to the file
                    snfile.write(sn + "\n")
                    # closes the file
            except FileExistsError:
                #logs that the file not found
                log.info("File not found")
                # creates the file
                with open(file, "x") as snfile:
                    # writes the sirial number to the file
                    snfile.write(sn + "\n")
                    # closes the file
            except Exception as e: #type: str
                # logs the unknow error
                log.critical("Unknow error: ", exc_info=True)

    # saves info the entered file
    def saveToFile(self, file: str, info: str, prefix: str):
        # logs that this function ran
        log.info("Running saveToFile in saveThingToFiles")
        # tries saving the info to the file
        try:
            # opens the file
            with open(file, "a") as f:
                # adds info to file
                f.write(prefix + info + "\n")
        # creates the file and adds the info
        except FileExistsError:
            # logs that the file was not found
            log.warning("file not found")
            # opens the file
            with open(file, "x") as f:
                # adds the info
                f.write(prefix + info + "\n")
        except Exception as e:
            #logs the unknow error
            log.critical("Unknown error: ", exc_info=True)
            
    # saves user provided info
    def saveUserInfo(self, file: str, info: list[str]):
        # logs that this function ran
        log.info("Running saveUserInfo in saveThingToFiles")
        # checks if the file exists
        if(os.path.exists(file)):
            # clears the file and saves the new info
            saveThingToFiles.clearFile(self, file)
            saveThingToFiles.saveToFile(self, file, info[0], "Specific hour: ")
            saveThingToFiles.saveToFile(self, file, info[1], "Days needed to pass: ")
            saveThingToFiles.saveToFile(self, file,info[2], "Daily check: ")
        else:
            # creates the file and saves the new info
            saveThingToFiles.saveToFile(self, file, info[0], "Specific Time: ")
            saveThingToFiles.saveToFile(self, file, info[1], "Days needed to pass: ")
            saveThingToFiles.saveToFile(self, file,info[2], "Disable everyday: ")

    def saveToList(self, file: str, info: str):
        # logs that this function ran
        log.info("Running saveToList in saveThingToFiles")
        # tries saving the info to the file
        try:
            # opens the file
            with open(file, "a") as f:
                # adds info to file
                f.write(info + ", ")
        # creates the file and adds the info
        except:
            # opens the file
            with open(file, "x") as f:
                # adds the info
                f.write(info+ ", ")

    
    def saveIQinfo(self, file:str, info: list[str], prefix: list[str]):
        # logs that this function ran
        log.info("Running saveIQinfo in saveThingToFiles")
        # checks if the file exist
        if(os.path.exists(file)):
            # check if the user entered all the required info
            if(info[0] != "" and info[1] != "" and info[2] != "" and info[3] != ""):
                # removes the file
                os.remove(file)
                # recreates the file and adds API token to the file
                saveThingToFiles.saveToFile(self, file, info[0], prefix[0])
                # adds the API url to the file
                saveThingToFiles.saveToFile(self, file, info[1], prefix[1])
                # adds the disable ID to the file
                saveThingToFiles.saveToFile(self, file, info[2], prefix[2])
                # adds the project ID to the file
                saveThingToFiles.saveToFile(self, file, info[3], prefix[3])
            # runs only if something was changed
            elif(info[0] != "" or info[1] != "" or info[2] != "" or info[3] != ""):
                # I dont remeber how this works
                i = 0
                for x in info:
                    if(x != ""):
                        with open(file, "w") as F:
                            val = file.find(prefix[i])
                            F.seek(val)
                            e = prefix[i] + x
                            F.write(e)
                    i = i + 1
                else:
                    pass
            else:
                pass
        else:
            # saves the API token to the file
            saveThingToFiles.saveToFile(self, file, info[0], prefix[0])
            # adds the API url to the file
            saveThingToFiles.saveToFile(self, file, info[1], prefix[1])
            # adds the disable ID to the file
            saveThingToFiles.saveToFile(self, file, info[2], prefix[2])
            # adds the project ID to the file
            saveThingToFiles.saveToFile(self, file, info[3], prefix[3])


    # clears the entered file
    def clearFile(self, file: str):
        # logs that this function ran
        log.info("Running clearFile in saveThingToFiles")
        # deletes the entered file
        os.remove(file)

    # changes a line in the file   
    def changeLineInFile(self, File: str, info: str, infoToChange: str ):
        # logs that this function ran
        log.info("Running changeLineInFile in saveThingToFiles")
        try:
            # opens the file
            with open(File, "w") as f:
                lines = f.readlines()
                i = 0
                # looks for the line to change
                for x in lines:
                    if(x.find(infoToChange)):
                        # set the line to the provided info
                        lines[i] = info
                        # writes lines to the file
                        f.writelines(lines)
                        break
                    else:
                        i = i + 1
        except FileNotFoundError:
            # log that the file was not found
            log.warning("File not found")
            # creates the file then opens it
            with open(File, "x") as f:
                lines = f.readlines()
                i = 0
                # looks for the line to change
                for x in lines:
                    if(x.find(infoToChange)):
                        # sets the line to the provided info
                        lines[i] = info
                        # writes lines to the file
                        f.writelines(lines)
                        break
                    else:
                        i = i + 1
        except Exception as e:
            log.critical("Unknow error: ", exc_info=True)
            
    # This takes a string and saves it into memory       
    def saveFileToMemory(self, text:str) -> io.StringIO:
        # logs that this function ran
        log.info("Running saveFileToMemory in saveThingToFiles")
        # makes the place where it will store the string in memory
        tempFile = io.StringIO()
        # writes the text to the place in memory
        tempFile.writelines(text)
        # returns the place in memory
        return tempFile
