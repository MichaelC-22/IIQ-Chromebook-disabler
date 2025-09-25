import requests
import datetime as date
import json
import logging as log
import datetime

class incidentIQ:
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
    # logs that the class was loaded
    log.info("loaded incidentIQ")
    
    def getIIQinfo(self) -> list[str]:
        # logs that the function started
        log.info("running getIIQinfo in incidentIQ")
        # reads the IQ info file and adds the info to a list
        try:
            IQinfo = []
            # opens the file
            with open("IIQ_info.txt", "r") as file:
                # reads the lines
                IQinfo = file.readlines()
            i = 0
            # adds each line to the list
            for x in IQinfo: # type: ignore # type: str
                # finds where the : is and adds one
                temp_int = IQinfo[i].find(":") + 1
                temp_str = IQinfo[i]
                # gets everything after the temp_int
                IQinfo[i] = temp_str[temp_int: ]
                # removes \n
                IQinfo[i] = IQinfo[i].strip("\n")
                IQinfo[i] = IQinfo[i].strip()
                i = i + 1
            return IQinfo
        except IndexError:
            # logs that the Incident IQ file is empty
            log.warning("Incident IQ information was missing from the IIQ_info file.")
            # tells the user that the incident IQ file is empty
            print("The Incident IQ information file is empty.\nType change IIQ info into the command line.\nEnter the required information and then type restart daily check.\n")
            return [""]
        except Exception:
            # logs the unknown error
            log.critical("Unknown error: ", exc_info=True)
            return [""]
        
            
    # uses the file to disable all assets in the file
    def disable(self, SN: str):
        # logs that the function started
        log.info("Running disable in incidentIQ")
        # gets the entered data from IQinfo.txt
        IQinfo:list[str] = incidentIQ.getIIQinfo(self)
        # The API Token
        APIToken:str = IQinfo[0]
        # the API url
        API_url:str = IQinfo[1]
        # the ID of the asset status disabled
        disabledID:str = IQinfo[2]
        # URL for the GET request to IQ for the serial number
        SN_URL = API_url + "/assets/serial/" + SN
        # Headers for the serial number request
        SN_headers = {"Authorization": "Bearer " + APIToken, "Content-Type": "application/json", "perfer": "code=200", "Accept": "application/json" }
        # gets a computer's information from IIQ based on the computers SN
        SN_request = requests.get(SN_URL, headers=SN_headers)
        if(SN_request.status_code == 200):
            # makes a directory out of the response from the server
            file: dict[str, str]= json.loads(SN_request.text)
            # creates the URL of the specific device
            asset_url =  API_url + "/assets/" + file["Items"][0]["AssetId"] # type: ignore
            # sets statusTypeID to the disabled ID
            file["Items"][0]["StatusTypeId"] = disabledID # type: ignore
            # sets assetStatusTypeID to the disabled ID
            file["Items"][0]["Status"]["AssetStatusTypeId"] = disabledID # type: ignore
            # removes not important stuff
            file.pop("ItemCount")
            file.pop("UserToken")
            file.pop("RequestDate")
            file.pop("ExecutionTime")
            file.pop("StatusCode")
            file.pop("ServerName")
            file.pop("ProcessId")
            file.pop("Properties")
            file.pop("Metadata")
            del file["Items"][0]["CustomFieldValues"] # type: ignore
            del file["Items"][0]["DataMappings"] # type: ignore
            # creates a string named tempfile and sets it to the remains of file
            tempfile = json.dumps(file)
            # removes the first 11 characters and the last few lines then adds a } to the end of the string
            tempfile = tempfile[11:len(tempfile) - (29 + len("""AssetAuditPolicyStatusSortOrder": 0, 
                                                             "LastVerificationSuccessful": false, "TotalCost": 
                                                             {"AssetId": ""}, 
                                                             "CategoryId": """))] + "}"
            # headers for the change assest status request 
            asset_headers = {
                 "Accept": "application/json", 
                 "Content-Type": "application/json", 
                 "Authorization": "Bearer " + APIToken,
                 "Prefer": "code=200"
                 }
            #sends the change asset status to IIQ
            disableRequest = requests.post(url=asset_url, data=tempfile, headers=asset_headers)
            # logs the status code of the disable request
            log.info(SN + " status code: " + str(disableRequest.status_code))
        else:
            # logs the status code of the disable request
            log.info(SN + " status code: " + str(SN_request.status_code))
                
    # converts the user's time to minutes
    def convertToMinutes(self) -> int:
        # logs that the function started
        log.info("Running convertToMinutes in incidentIQ")
        # opens the user file
        with open("userinfo.txt", "r") as file:
            # reads the first line in the file and sets it to time
            time = file.readline()
            # removes specific hour from time
            time = str(time).replace("Specific hour:", "")
            # sets every letter left in time to lower case
            time = time.lower()
            # removes spaces from time
            time = time.strip()
        # checks if the user's time is am
        if(time.find("a") != -1):
            # removes am from time
            time = time.replace("am", "")
            # splits the hours and minutes
            time = time.split(":")
            # mutliples the hours by 60 then adds the minutes
            time = float(time[0]) * 60 + float(time[1])
        # checks if the user's time is pm
        elif(time.find("pm") != -1):
            # removes hte pm from time
            time = time.replace("pm", "")
            # splits the hours and minutes
            time = time.split(":")
            # checks if the hour is equal to 12
            if(int(time[0]) == 12):
                # mutliples the hours by 60 then adds the minutes
                time = float(time[0]) * 60 + float(time[1])
            else:
                # adds 12 to the hour and then mutliples the hours by 60 then adds the minutes
                time = (float(time[0]) + 12) * 60 + float(time[1])
        else:
            # splits the hours and minutes
            time = time.split(":")
            # mutliples the hours by 60 then adds the minutes
            time = float(time[0]) * 60 + float(time[1])
        # returns the total minutes of the user's time
        return int(time)


    # copmpaies the chomebook's last check out date to the current date
    def monthChecker(self, ModifiedDate: str, user_Time: int):
        # logs that the function started
        log.info("Running monthChecker in incidentIQ.")
        # creates a temp str to be used later
        tempstr = str(ModifiedDate)
        # Only takes things before the T in ModifiedDate
        ModifiedDate = tempstr[0:int(tempstr.find("T"))]
        # makes ModifiedDate into a list
        ModifiedDateList:list[str] = ModifiedDate.split("-")
        # gets the current time
        currentDate = date.date.today()
        # changes the time the chromebook was last check out to a date type
        ChromebooksDate = date.date(int(ModifiedDateList[0]), int(ModifiedDateList[1]), int(int(ModifiedDateList[2]) + user_Time))
        # checks if the current date is greater then the chromebook's date
        if(currentDate > ChromebooksDate):
            # returns the current date
            return currentDate
        else:
            # returns the chromebooks date
            return ChromebooksDate

    def disableTheChromebooks(self, SNFILE: str):
        # logs that the function started
        log.info("Running disableTheChromebooks in incidentIQ.")
        # gets the entered data from IQinfo.txt
        IQinfo = incidentIQ.getIIQinfo(self)
        # The API Token
        APIToken = IQinfo[0]
        # the API url
        API_url = IQinfo[1]
        # default values 
        ModifiedDate = ""
        status = ""
        hasOwner = False
        try:
            # gets today's date
            today = date.date.today()
            # opens the SN file to read it
            file = open(SNFILE, "r")
            # creates a list of all the lines in the file
            file = file.readlines()
            # goes through each element in the list
            for line in file:
                # removes whitespaces and make sure every letter is up chase
                line = line.strip().upper().replace("\n","")
                # URL for the GET request to IQ for the serial number
                SN_URL = API_url + "/assets/serial/" + line.strip()
                # Headers for the serial number request
                SN_headers = {"Authorization": "Bearer " + APIToken, "Content-Type": "application/json", "perfer": "code=200", "Accept": "application/json" }
                # sends the serial number request to IQ
                SN_request = requests.get(SN_URL, headers=SN_headers)
                if(SN_request.status_code == 200):
                    #creates a directory from the response from the server
                    device: dict[str, str] = json.loads(SN_request.text)
                    # sets modifiedDate to a directory of the first customeFieldValue which contains the last login in data
                    ModifiedDate = json.loads(device["Items"][0]["CustomFieldValues"][0]["Value"]) # type: ignore
                    # gets the last login date from the directory
                    ModifiedDate:str = ModifiedDate[0]["LastLoginDate"] # type: ignore
                    # gets the status from the device
                    status = device["Items"][0]["Status"]["Name"] # type: ignore
                    try:
                        # checks if the device has an Owner
                        if(device["Items"][0]["OwnerId"] != ""): # type: ignore
                            hasOwner = True
                    except:
                        continue
                    # selects the date from the string and creates a list divided by the - character
                    ModifiedDateList:list[str] = ModifiedDate.split("-")
                    # makes modified date a datetime data type
                    Date = date.datetime(int(ModifiedDateList[0]), int(ModifiedDateList[1]), int(ModifiedDateList[2]))
                    # disables the chromebook if everything below is true
                    if(Date != today and status != "Disabled" and hasOwner == True):
                        # disables the chromebook in both Incident IQ and in Google admin
                        incidentIQ.disable(self, line)
                        # prints the disabled chromebook
                        print(line + " has been disabled.\n")
                        # logs the disabled Chromebook
                        log.info(line + " has been disabled.")
                    else:
                        log.info(line + " was skipped.")
                else:
                    log.info(line + " status code: " + str(SN_request.status_code))
        except IndexError:
            # logs that the serial number file was empty
            log.warning("Serial number file was empty.")
            # tells the user that the serial number is empty and how to fix it
            print("The Serial number file is empty. Type enter serial numbers into the command line to add Serial numbers to the file")
        except FileNotFoundError:
            # logs that the serial number file was not created
            log.warning("The serial number file was not created")
            # tells the user that the serial number is not created and how to fix it
            print("The file was not created.\nTyping enter serial nubmers into the command line to create the file.")
        except Exception:
            # logs the unknown error 
            log.critical("Unknow error: ", exc_info=True)
