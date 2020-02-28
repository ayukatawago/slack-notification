from slack import WebClient


class SlackBot:
    def __init__(self, api_token):
        self.client = WebClient(api_token)

    def post_message(self, channel, message):
        response = self.client.chat_postMessage(
            channel=channel,
            text=message)
        assert response["ok"]
        assert response["message"]["text"] == message
