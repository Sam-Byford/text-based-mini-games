from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import os

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
        if bodyLower == 'start game':
            message = "Hello and welcome to Text Based Mini Games by Murray's Angels"
            message += "\n\nPlease enter one of the following options;"
            message += "\n\n'Play Hangman' - A simple game of Hangman"
            message += "\n'Play Survive' - Play the text based adventure game 'Survive The Midlands'"
            resp.message(message)
            start = True
            return str(resp)
        else:
            resp.message("Please enter one of the following commands; \n - 'Start Game'")
            return str(resp)

    if bodyLower == 'play hangman':
        currentGame = "Hangman"
    elif bodyLower == 'play survive':
        currentGame = "Survive"
    elif bodyLower == 'reset':
        currentGame = "Nothing"
        resp.message("Thanks for playing!")
        start = False
        return str(resp)

    if currentGame == 'Hangman':
            resp.message(HangmanInit(bodyLower))
            print(resp.message)
            return str(resp)
    elif currentGame == 'Survive':
            resp.message(SurviveInit(bodyLower))
            print(resp.message)
            return str(resp)
    else:
        resp.message("Error no game selected")

    return str(resp)

def HangmanInit(UserAction):
    print("Hangman Initialised")
    return 'This is hangman! User Input: ' + UserAction

def SurviveInit(UserAction):
    print("Survive Initialised")
    return 'This is Survive The Midlands! User Input: ' + UserAction


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv('PORT', 5000), host='0.0.0.0')