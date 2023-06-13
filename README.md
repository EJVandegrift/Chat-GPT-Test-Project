# Chat-GPT-Test-Project

Preface: I have never had to create a README file to explain my code, but here it goes.

'credentials.json' and 'token.json':

Both of these json files are necessary for accessing Google's API. I changed out identifiable information to "DUMMY_STRING" within the files, though.


Plan / Process:

The biggest challenge regarding this project was how to feed ChatGPT the data. Because I would be using openai's API in my project, I figured the best way to do so would be to feed the data internally. So, I used Google's API to access spreadsheets.
In order to do so, I, as the developer, had to go through an authentication process to get credentials and a token. Using the the spreadsheets API, I drew the information from the spreadsheet and stored it within an empty textfile within the project. This way, I could simply take that
newly stored information within the text file and feed it to ChatGPT within the main file.

I had messed with ChatGPT on the web to see how easily it could process and understand data, mostly to see if there was a specific way I needed to format the information for it to be legible to the bot. I had tested copying and pasting from the spreadsheet directly into ChatGPT and also
pasting it into a document, and then copying it and pasting it into chatGPT. Both methods worked, meaning that, although ugly to the human eye, feeding the data from the text file within the project into the bot would not cause any issues.

The next thing I tested was giving ChatGPT the data before the user interacts with the program while also not recieving any responses - essenestially preloading the necessary information. This was done by using one of ChatGPT's API functions to tell it
what it's role will be and who it is interacting with, followed by taking the data we had stored and feeding it that as well. None of these actions warranted a response, which is only obtained if the develoeper asks for such, so after that, the program would than begin its interaction
with the user.


The flow of the process looks something like this

1. Get spreadsheet info using Google API
2. Through a function, store that data within the local text file
3. Begin interaction with ChatGPT using the API to tell it what it will be used for + sending it the data
4. Prompt user to ask ChatGPT question
5. Based on users response, either end the conversation or recieve a response from ChatGPT


Current State:

If a 3rd party wanted to use this, they would create a google spreadsheet containing their data and share permissions with whichever google account was authorized to use the GoogleAPI. Currently, they would need to also specify which page / sheet in the entire spreadsheet has the data, but 
with maybe 2 additional hours of work, I could implement functionality that looks at all the sheets in the spreadsheet for data, rather than the one the user specifies. With those necessities, they would be able to use the program.

ChatGPT is completely setup and ready for use within the program and so is the spreadsheet functionality. If the user wanted to, they could have a full blown conversatoin with the bot as if they were using the web application, and if they wanted to use the bot to look at data for help,
they could do so as well.


One thing I would have added if I weren't stretched for time this week is a tester class. There are a couple functions within the mainfile that aren't the most straightforward, so I believe it would be helpful to have a tester class to experiment with and tweak my methods in an isolated space.

Quirks of openai's current API for ChatGPT:

If you use chatGPT on the web, you can send a continous stream of messages so long as each message isn't larger than 4096 tokens of space. While using the API, however, ChatGPT treats each message / prompt as its own enviroment or interaction, so if you try to send a follow up question,
it will not understand what you are talking about because it will have forgotten everything about your previous message. The way to combat this, as reccomended by openai, is to create and store what is basically a message log. Each message, either from the user or ChatGPT, gets stored
in this message log, an array or list, and then when the user wants to send a new message, everything from that log gets added on to the message to give ChatGPT the context of what the conversation was about. Although the best solution currently, the issue is that we are still limited
by the 4096 token maximum length for a message, and if you want to seperate the information into mulitple messages to not exceed that limit  - as I initially planned to do - only the current question will be answerable / understable by ChatGPT, as it will have forgotten everything else.

As I understand it, if a data set is larger than the 4096 token limit, it will not be possible for ChatGPT to function. Even if it is smaller than that limit, each message between the user and ChatGPT is essenestially being glued on to the top of all the previous messages and then sent 
together until your new messages send you over the limit.
