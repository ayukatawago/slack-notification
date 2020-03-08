from slack import WebClient


class SlackApiWrapper(WebClient):
    def __init__(self, api_token):
        super().__init__(api_token)

    def post_message(self, channel, message):
        response = self.chat_postMessage(
            channel=channel,
            text=message)
        assert response["ok"]

    def post_attachment_message(self, channel, blocks, attachments):
        response = self.api_call(
            'chat.postMessage',
            json=dict(
                channel=channel,
                blocks=blocks,
                attachments=attachments
            )
        )
        assert response["ok"]

    def update_message(self, channel, ts, blocks, attachments):
        response = self.api_call(
            'chat.update',
            json=dict(
                channel=channel,
                ts=ts,
                blocks=blocks,
                attachments=attachments
            )
        )
        assert response["ok"]
