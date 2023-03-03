import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import datetime
import time

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")


@app.message("wake me up")
def say_hello(client, message):
    # Unix Epoch time for September 30, 2020 11:59:59 PM
    date_time = datetime.datetime(2023, 3, 3, 16, 50)
    test = time.mktime(date_time.timetuple())
    when_september_ends = 1601510399

    channel_id = message["channel"]
    client.chat_scheduleMessage(
        channel=channel_id,
        post_at=test,
        text="This is a 5 minute reminder to book the court."
    )

@app.message("hello")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")

@app.event("reaction_added")
def get_info(event):
    print(event)
    message_obj = event['item']

    x = app.client.reactions_get(
        token=os.environ.get("SLACK_USER_TOKEN"),
        channel=message_obj["channel"],
        timestamp=message_obj["ts"],
    )

    print(event['reaction'])
    print(x['message']['text'])

    


@app.event("team_join")
def ask_for_introduction(event, say):
    welcome_channel_id = "C12345"
    user_id = event["user"]
    text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel."
    say(text=text, channel=welcome_channel_id)
    



if __name__ == "__main__":
    # Start your ap
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()