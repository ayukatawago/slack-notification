from bot.trellowrapper import TrelloWrapper
from bot.slackbot import SlackBot
from slackutil.slackbuilder import SlackBlockBuilder, SlackAttachmentBuilder
import config


def create_trello_block():
    return SlackBlockBuilder().add_section("*Today's task*").add_divider().build()


def create_trello_attachments(cards):
    builder = SlackAttachmentBuilder()
    for card in cards:
        item = SlackBlockBuilder().add_section(card).build()
        builder.add_item(item)
    return builder.build()


def main():
    # get cards from Trello
    trello = TrelloWrapper(config.trello_api_key, config.trello_token)
    cards = trello.get_todo_cards('TODO')

    # notify to slack
    slack = SlackBot(config.slack_api_token)
    blocks = create_trello_block()
    attachments = create_trello_attachments([card.name for card in cards])
    slack.post_attachment_message(
        channel='#todo',
        blocks=blocks,
        attachments=attachments
    )


if __name__ == '__main__':
    main()
