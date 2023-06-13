# importing libraries / modules
import os
import openai


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Gives access to various permissions within the spreadsheet - only using the one for editing + viewing
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# keys / IDs for using APIs
SPREADSHEET_ID = "DUMMY_SPREADSHEET_1"
SPREADSHEET_ID2 = "DUMMY_SPREADSHEET_2"

openai.api_key = "DUMMY_KEY"

# Easier to write line break in terminal
def lineBreak():
    print("\n")

# Makes ChatGPT's responses more readable in terminal by setting max line length
def responseFormatting(text: str, lineBreakLength: int) -> str:
    newText = ""
    lineBreakCounter = 0
    counter = 0
    while (counter < len(text)): # Checking if we have all the chars from original string

        if(lineBreakCounter >= lineBreakLength and text[counter - 1] == " "): # New line and indent if we have exceeded line length and aren't in middle of typing word
            newText += "\n\t" + text[counter]
            lineBreakCounter = 0 # Reseting the counter for the next line
            counter += 1

        elif(lineBreakCounter >= lineBreakLength and text[counter - 1] != " "): # Next char in str if we are in middle to typing word but exceeded line length
            # We are not resetting lineBreakCounter - waiting for word to finish typing
            newText += text[counter]
            counter += 1


        else: # Type next char and increment variable if below line length
            newText += text[counter]
            lineBreakCounter += 1
            counter += 1
    
    return newText

# Making rows from the spreadsheet's columns in the form of str's - recursive function
def addAllColumns(list: list, length: int, counter: int, line: str) -> str: 
    # counter and line should be set to 0 and "" respectivley
    if(counter < length):
        line += list[counter] + " " # adding cell info to str
        return addAllColumns(list, length, counter + 1, line)
    else:
        return line



def GPTInteraction(data: str):
    '''' ChatGPT, when not using the web application, will register
         each prompt / message as its own, standalone instance, losing
         the context of any previous messages. For that reason, we must
          store and add-on the messages of the entire interaction so there is an
          intelligble, continous flow of conversation. Otherwise, it will
          not understand follow up questions / messages. This also means
          that the data sent to ChatGPT needs to be continously sent with
          each message. Because of this, each message the user sends has
          to include the text of the previous conversation - which is what
          we are doing under the hood. Any message containing more than 4096 tokens of 
          information, however, will crash ChatGPT.'''

    messages = [] # List to store previous messages

    data = divideData(dataToDivide=data) # Seperating data into small, digestable chunks for chatGPT to use 
                                         #IMPORTANT: This has a null impact, because we must send all information from the past conversation for context

    messages.append({"role": "system", "content": '''You are an assistant helping with data about housing through various cities in Wisconsin.
                                                     I will send the data to you over multiple messages,
                                                     and I will say 'I am finished sending all the data.' when all the data has been sent. All the information is continuous from the last
                                                     message, so it is all from the same data source.'''})

    for entry in data:
        messages.append({"role": "system", "content":entry})

    messages.append({"role": "system", "content": "I am finished sending all the data."})




    # Beginning of actual conversation between ChatGPT and user
    print("ChatGPT is ready for use! Ask a question or enter 'break()' to finish your conversation!\n\n")
    message = input("User Response:\n\n\t")

    while message != "break()": # Won't stop interaction unless user types the key phrase
        messages.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages) # ChatGPT's response based on what the user said in 'message'

        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        lineBreak
        print("\n\nChatGPT Response:\n\n\t" + responseFormatting(text=reply, lineBreakLength=50) + "\n\n") # formatting the response to the terminal and printing it
       

        message = input("User Response: ") # Starting the next loop with the users response
    

# Function to write info from 'values' into the text file in our project - 'data.txt' in our case
def writeFile(location: str, values: list[str]):
    # Opening the data file so we can add text to it
    with open(location, "w") as dataFile:
        # Writing the information into the file for chatgpt to use
        for row in values:
            newLine = addAllColumns(list=row, length=len(row), counter=0, line="")
            dataFile.write(newLine + "\n")

# making a list of strings that draws infomration from the text file we wrote into
def readFile(location: str) -> list[str]:
    with open(location) as info:
        fileContents = info.readlines()
        return fileContents


''''Because ChatGPT can only handle 4096 tokens of data, this function is made to
    split the data we need into smaller, digestable chunks. This would be extremely
    useful in the web application where you can have multiple messages without needing
    to send all the text from the conversation, but each 'instance'/'conversation' using the API
    can only handle 4096 tokens in total. Essentially, this function doesn't make a difference.
    '''
def divideData(dataToDivide: str) -> list[str]: # Takes a str containing all our data and breaks into a list of managble segments
    wordCount = len(dataToDivide)
    lowerLimit = 0
    constant = 14000 # This is the length each segment will be until the  final segment is reached -> 15,000 chars is roughly 4096 tokens, so our segments will be just under that to avoid crashing
    upperLimit = 14000
    splitData = [] 
    if(len(dataToDivide) > 13226): # If the data is too big to be sent in one message, break into smaller chunks

        while(wordCount > 0):
            splitData.append(dataToDivide[lowerLimit:upperLimit]) # Making a substring of the data from the lower limit to the upperlimit
            lowerLimit = upperLimit # for the next segment, the lower limit will move to where the upper limit was

            ''' We must check to see if we have enough data left to make a full increment - 'constant' - or
                if we are too close to the end of the data where we would go out of the bounds of the str'''
            
            # We have enough data left for a full increment
            if(wordCount > constant): 
                upperLimit += constant  , # We increment our upper limit by the constant
                wordCount -= upperLimit - lowerLimit # The amount of data we have left is subtracted by the distance between the lower and uppper limit - 'constant'
            
            # We don't have enough data for a full increment
            else:
                upperLimit += wordCount + 1 , # The upper limit goes until the end of the str 
                wordCount = 0 # we have finished all the data by this point

    # If we don't need to break up the data, just add it all to the first spot in the list
    else:
        splitData.append(dataToDivide)
                
    return splitData



def main():

    credentials = None

    # If we have a token we can authenticate and use, load it
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)
        print("This is running 1 \n")


    if credentials == False:
        print("This is running 2 \n")
        # If the credentials are expired, refresh them
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        # If the credentials don't exist in the first place, export them so we have a usable one
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json()) 



    try:
        # Of googles API platforms, we are selecting google sheets
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        # Getting selected values from the spreadsheet
        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID2, range="Sheet1").execute() # Sheet 1 refers to the specific page / sheet in the entire spread sheet
        values = result.get("values", [])


        # FOR FUTURE EJ: Why not set the values from the spreadsheet into a variable containging a list rather than making it two steps?
        writeFile(location="data.txt", values=values)

        
        data = ""
        for row in readFile(location="data.txt"):
            data += row
            



        GPTInteraction(data=data)


    except HttpError as error:
        print("\n")
        print(error)




if __name__ == "__main__":
    main()
