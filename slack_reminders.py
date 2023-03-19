import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from datetime import datetime, timedelta
import time

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

emoji_idx_dict = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 
                  'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
                   'grinning': 11, 'smiley': 12 }

@app.command("/echo")
def repeat_text(ack, respond, command):
    # Acknowledge command request
    ack()
    respond(f"{command['text']}")


@app.message("wake me up")
def say_hello(client, message):
    # Unix Epoch time for September 30, 2020 11:59:59 PM
    date_time = datetime.datetime(2023, 3, 9, 17, 45)
    test = time.mktime(date_time.timetuple())
    when_september_ends = 1601510399

    channel_id = message["channel"]
    client.chat_scheduleMessage(
        channel=channel_id,
        post_at=test,
        text="This is a 3 minute reminder to book the court."
    )

@app.message("hello")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")

@app.event("reaction_added")
def get_info(event, client, say):
    message_obj = event['item']

    x = app.client.reactions_get(
        token=os.environ.get("SLACK_USER_TOKEN"),
        channel=message_obj["channel"],
        timestamp=message_obj["ts"],
    )
    print(event)
    print(event['reaction'])
    print(x['message']['text'])

    reaction = event['reaction']
    times = x['message']['text'].split('\n')

    if reaction not in emoji_idx_dict.keys():
        say('The reaction you have picked is not a valid reaction. Please try again!')
    else:
        court = times[0][:times[0].find('-')]
        selected = times[emoji_idx_dict[reaction]].strip()
        am_flag = True if selected[-2:] == 'AM' else False
        time_parse = int(selected[selected.find(': ') + 2: selected.find(' -') + 1])
        two_days = datetime.now() + timedelta(days=2)
        date_time = datetime(two_days.year, two_days.month, two_days.day, time_parse if am_flag else time_parse + 11, 55)

        channel_id = event['item']['channel']
        client.chat_scheduleMessage(
            channel=channel_id,
            post_at=time.mktime(date_time.timetuple()),
            text=f"This is a 5 minute reminder to book {court}"
        )

        say(f"A reminder to book {court} has been created for {date_time}")

        



    


@app.event("team_join")
def ask_for_introduction(event, say):
    welcome_channel_id = "C12345"
    user_id = event["user"]
    text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel."
    say(text=text, channel=welcome_channel_id)
    



if __name__ == "__main__":
    # Start your ap
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()