from slack import WebClient


class SlackBot:
    def __init__(self, api_token):
        self.client = WebClient(api_token)

    def post_message(self, channel, message):
        response = self.client.chat_postMessage(
            channel=channel,
            text=message)
        assert response["ok"]

    def post_attachment_message(self, channel, blocks, attachments):
        response = self.client.api_call(
            'chat.postMessage',
            json=dict(
                channel=channel,
                blocks=blocks,
                attachments=attachments
            )
        )
        assert response["ok"]
