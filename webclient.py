from slackeventsapi import SlackEventAdapter
from slack import WebClient
import os
import yaml

config = yaml.load(open('slack.conf', 'r'))


# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = config['signing-secret']
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = config['bot-token']
slack_client = WebClient(slack_bot_token)

# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    print("Got message: " + message.get('text'))
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        response = slack_client.chat_postMessage(
          channel='#random',
          text="Hello world!")
        assert response["ok"]
        assert response["message"]["text"] == "Hello world!"


# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    response = slack_client.chat_postMessage(
      channel='#random',
      text=text)

# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)