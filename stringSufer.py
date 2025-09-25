import datetime
import io
import logging as log

class stringSurfer:
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
    log.info("Loaded stringSufer")
    # gets text that is after other text
    def getAfter(self, line: str, text: str, SC:list[str]):
        # logs that this function ran
        log.info("Running getAfter in stringSufer")
        # removes the text from the start of the line to the entered text
        info = line[0] + "" + line[line.find(text) + 1:]
        # replaces entered charater with nothing
        for x in SC: #type: str
            info = info.replace(x, "")
        # repalces spaces with nothing
        info = info.replace(" ", "")
        return info

        # used to find specific text in a string
    def getTextFromFile(self, origanl_text: str, text: str, lastChar: str, removeSpecialCharacters:list[str]) -> str:
        # logs that this function ran
        log.info("Running getTextFromFile in stringSufer")
        # checks to see if there is a ,
        if(text.find(",")):
            # Finds position of the , and adds one
            temp_int = text.find(",") + 1
            # creates a temp string to read from
            temp_str = str(origanl_text)
            # finds the inputted text
            info = temp_str.find(text)
            # removes the selected text from the oringanl text using the charater at the end of the text. 
            info = temp_str[int(info):int(temp_str.find(lastChar, int(info + temp_int)))]
            # replaces remove charater with replace charater if they are entered
            info = stringSurfer.getAfter(self, info, text, removeSpecialCharacters)
            # returns the text
            return info
        else:
            # creates a temp string to read from
            temp_str = str(origanl_text)
            # finds the inputted text
            info = temp_str.find(text)
            # removes the selected text from the oringanl text using the charater at the end of the text. 
            info = temp_str[int(info):int(temp_str.find(lastChar, info))]
            # replaces remove charater with replace charater if they are entered
            info = stringSurfer.getAfter(self, info, text, removeSpecialCharacters)
            # returns the text
            return info

    # gets all the text from a file and makes it a list
    def getTextFromFileToList(self, file: str) -> list[str]:
        # logs that this function ran
        log.info("Running getTextFromFileToList in stringSufer")
        templist:list[str] = []
        try:
            # opens the file
            with open(file, "r") as tempFile:
                # reads the lines of the file
                tempFile = tempFile.readlines()
                tempFile = str(tempFile)
                # looks for a ,
                if(tempFile.find(",")):
                    # creats a list by splitting the ,
                    tempFile.split(",")
                    # adds the items in tempFile to templist
                    for x in tempFile:
                        templist.append(x)
                    return templist
                else:
                    # adds the line to the list
                    templist.append(tempFile)
                    return templist
        # lets the user know there is no file
        except FileNotFoundError:
            # logs that the file was not found
            log.warning("File was not found")
            print(file + " has not been created yet. If this is your first time running the program make sure you followed the setup process correctly.")
            return [""]
        # for any unexpected errors
        except Exception as e: #type: str
            # logs any other errors
            log.critical("Unknown error: ", exc_info=True)
            return[""]
            
    def readLineFromFile(self, file: str, lineNumber: int) -> str:
        # logs that this function ran
        log.info("Running readLineFromFile in stringSufer")
        try:
            with open(file, "r") as line:
                line = line.readlines()
            return line[lineNumber]
        except FileNotFoundError:
            # logs that the file was not found
            log.warning("file was not found")
            print(file + " has not been created yet. If this is your first time running the program make sure you followed the setup process correctly.")
            return ""
        except Exception as e:
            # logs the unknow error
            log.critical("Unknow error: ", exc_info=True)
            return ""
            
    def removeStringFromline(self, file: str, word: str, lineNumber: int) -> str:
        # logs that this function ran
        log.info("Running removeStringFromline in stringSufer")
        try:
            tempLine = str(stringSurfer.readLineFromFile(self, file, lineNumber))
            tempLine = tempLine.replace(word, "")
            tempLine = str(tempLine)
            return tempLine
        except FileNotFoundError:
            # logs that the file was not found
            log.warning("File was not found")
            print(file + " has not been created yet. If this is your first time running the program make sure you followed the setup process correctly.")
            return ""
        except Exception as e:
            # logs the unknow error
            log.critical("Unknow error: ", exc_info=True)
            return ""
            
    # Edites a specific line in an saved string in memory   
    def editLineInMemory(self, lineNumber: int, text: str, file: io.StringIO) -> io.StringIO:
        # logs that this function ran
        log.info("Running editLineInMemory in stringSufer")
        # makes sure the entered string in memory will read from the begining
        file.seek(0)
        # makes a temporary list by reading all the lines in the string contains
        tempList = file.readlines()
        # gets the specific line the user wants to edit
        line = tempList[lineNumber - 1]
        # persurves everything before the colen
        positionOfColen = line.find(":") + 2 
        # persurves the comma at the end of the line  
        positionOfNewLine = line.find("\n") - 2
        # replaces the specific line with text and adds " " to sround the text
        tempList[lineNumber - 1] = line[:positionOfColen] + '"' + text + '"' + line[positionOfNewLine:]
        # makes a new memory location for the modified string to be stored
        newFile = io.StringIO()
        # writes the modified list to the new memory location
        newFile.writelines(tempList)
        # returns the memory locaiton
        return newFile
    
    # gets a value from a String IO file
    def getInfoFromLineInMemory(self, LineNumber: int, file: io.StringIO) -> str:
        # logs that this function ran
        log.info("Running getInfoFromLineInMemory in stringSufer")
        # moves to the start of the file
        file.seek(0)
        # reads the lines and creates a list
        tempList = file.readlines()
        # set line to what ever is on the line number - 1
        line = tempList[LineNumber - 1]
        # finds the last character
        #lastChar:int = line.find("\n") - 1
        # gets the information that is after the : and before the end of the line
        line = stringSurfer.getAfter(self, line, ":", ['"', ' ', ','])
        # clears the list
        tempList.clear()
        # removes white space
        line = str(line).strip()
        return line
    
    # removes a line from the StringIO file
    def removeLineFromMemory(self, lineNumber: int, file: io.StringIO) -> io.StringIO:
        # logs that this function ran
        log.info("Running removeLineFromMemory in stringSufer")
        # moves to the start of the file
        file.seek(0)
        # read the lines and makes a list
        tempList = file.readlines()
        # sets the lineNumber - 1 to nothing
        tempList[lineNumber - 1] = ""
        # creates a new StringIO file
        newFile = io.StringIO()
        # defult value for x
        x: str = ""
        # goes through the list and skips lines that contain nothing and writes lines that contain stuff
        for x in tempList:
            # skips lines the contain nothing
            if(x == ""):
                pass
            else:
                # writes the line to the new file
                newFile.writelines(x)
        # clears the list
        tempList.clear()
        return newFile
    
    # removes everything after a word in a io.StringIO file
    def removeEverythingAfterWordInMemory(self, word: str, file: io.StringIO) -> io.StringIO:
        # logs that this function ran
        log.info("Running removeEverythingAfterWordInMemory in stringSufer")
        # moves to the start of the file
        file.seek(0)
        # reads the lines from the file and makes a list
        tempfile:list[str] = file.readlines()
        # creates a temporary new StringIO file
        newFile = io.StringIO()
        # goes through the list and writes to the new file
        for x in tempfile: #type: str
            # checks if the word is found in x and that the word lenght is equal to 7
            if(x.find(word) >= 0):
                #removes a comma from the word and writes it to the new file
                newFile.write(x.replace(",", "") + "\n}")
                # stops the for loop
                break
            else:
                # writes x to file
                newFile.write(x)
        # returns the new file
        return newFile
    
    