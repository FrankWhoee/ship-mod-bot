import slack
import yaml

@slack.RTMClient.run_on(event='message')
def getReponse(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    if 'SHIP' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']
        text = ""
        if channel_id == 'CQHHB8909':
            text = f"Hello, thank you for the ship <@{user}>!"

        web_client.chat_postMessage(
            channel=channel_id,
            text=text,
            thread_ts=thread_ts
        )
config = yaml.load(open('slack.conf', 'r'))
slack_token = config['token']
rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()