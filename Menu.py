from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os

from hangman import hangman
from textAdventure import game

app = Flask(__name__)

start = False
reset = False
currentGame = ""

@app.route("/", methods=['GET'])
def test():
    return 'hello'

@app.route("/sms", methods=['GET','POST'])
def main():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    # Start our TwiML response
    global start
    global reset
    global currentGame
    resp = MessagingResponse()
    bodyLower = body.lower()

    if start == False:
        if bodyLower == '/start':
            message = "Hello and welcome to Text Based Mini Games by Murray's Angels"
            message += "\n\nPlease enter one of the following options;"
            message += "\n\n'/Play Hangman' - A simple game of Hangman"
            message += "\n'/Play Survive' - Play the text based adventure game 'Survive The Midlands'"
            resp.message(message)
            start = True
            return str(resp)
        else:
            resp.message("Please enter one of the following commands; \n - '/Start'")
            return str(resp)

    if bodyLower == '/play hangman' and currentGame != "Survive":
        currentGame = "Hangman"
    elif bodyLower == '/play survive' and currentGame != "Hangman":
        currentGame = "Survive"
    elif bodyLower == '/reset' and currentGame == "Nothing":
        currentGame = "Nothing"
        resetString = "Thanks for playing!" + u"😃"
        resp.message(resetString)
        start = False
        return str(resp)

    if currentGame == 'Hangman':
            hangmanResponse = HangmanInit(bodyLower)
            print(hangmanResponse)
            if hangmanResponse == "You failed. Try again next time" or hangmanResponse == "Well Done! You beat hangman":
                currentGame = "Nothing"
                hangmanResponse += "\n\nThanks for playing! "  u"😃"
                start = False
                resp.message(hangmanResponse)
                return str(resp)
            elif hangmanResponse == "/reset":
                currentGame = "Nothing"
                hangmanResponse = "Thanks for playing! " + u"😃"
                start = False
                resp.message(hangmanResponse)
                return str(resp)
            resp.message(hangmanResponse)
            return str(resp)
    elif currentGame == 'Survive':
            surviveResponse = SurviveInit(bodyLower)
            print(surviveResponse)
            if surviveResponse == "You push the door open. You remember there is no lock on the doors and you could have left at anytime. It was a push door and you were pulling on it. Congratulations you have escaped":
                currentGame = "Nothing"
                surviveResponse += "\n\nTo be continued... " + u"🤷‍♀️"
                surviveResponse += "\n\nThanks for playing!"
                start = False
                resp.message(surviveResponse)
                return str(resp)
            elif surviveResponse == "/reset":
                currentGame = "Nothing"
                surviveResponse = "Tom waits for your return...\n\nThanks for playing! " + u"😃"
                start = False
                resp.message(surviveResponse)
                return str(resp)
            resp.message(surviveResponse)
            return str(resp)
    else:
        resp.message("Error no game selected")

    return str(resp)

def HangmanInit(UserAction):
    return hangman.run_game(UserAction)

def SurviveInit(UserAction):
    return game.run_game(UserAction)


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv('PORT', 5000), host='0.0.0.0')
