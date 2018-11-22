# bobweb
Bobweb is a project which contains a telegram bot and a web page. The bot runs on python3 and the web page on django. The website is optional and shows various states of the bot, for example scoreboards. Requirements are listed in the requirements.txt file. The bot speaks only Finnish and no English translations are available for the time being. 

## Implemented features:
##### Elite feature
Everyday when clock is 13:37, users in the chat has the possibility to say send message "1337". The first person who does this gets += 1 score. The scores are converted to a rank in Finnish Defence Forces. 
##### Random chooser
Usage: Send the bot a message that has the options seperated with word 'vai' (or in English) and the bot returns one of those options at random. 
For example: 

me: option1 vai option2 vai option3

the bot: option2

##### Random proverbs
By sending message "viisaus" the bot will respond with random proverb. New proverbs can be saved to the bot by sending it a message "uusi viisaus: [your proverb here]"

### Installation
Set up the settings.json and run Python3 bob.py and you are ready to go. You will also need your own telegram bot that you can obtain from the @botfather. 