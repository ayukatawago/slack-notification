from datetime import datetime
from trelloutil.trellowrapper import TrelloWrapper
from slackutil.slackbot import SlackBot
from slackutil.slackbuilder import SlackBlockBuilder, SlackAttachmentBuilder
import config


def create_trello_block():
    block = SlackBlockBuilder()
    block.add_section("*Today's task*")
    block.add_divider()
    return block.build()


def create_trello_attachments(cards):
    today = datetime.now()
    builder = SlackAttachmentBuilder()
    for card in cards:
        list_name = card.get_list().name
        task_name = "`{}` {}".format(list_name, card.name)
        due_date = card.due_date.strftime("%Y/%m/%d")

        accessory = dict(accessory=dict(type="button",
                                        text=dict(type="plain_text",
                                                  text="complete",
                                                  emoji=True),
                                        value=card.id
                                        ))
        item = SlackBlockBuilder()
        item.add_section(task_name, accessory)
        item.add_context(due_date)

        if card.due_date.astimezone().date() < today.date():
            color = "#ff9900"
        else:
            color = "#00c300"
        builder.add_item(item.build(), color)
    return builder.build()


def main():
    # get cards from Trello
    trello = TrelloWrapper(config.trello_api_key, config.trello_token)
    cards = trello.get_todo_cards('TODO')

    # notify to slack
    slack = SlackBot(config.slack_api_token)
    blocks = create_trello_block()
    attachments = create_trello_attachments(cards)
    slack.post_attachment_message(
        channel='#todo',
        blocks=blocks,
        attachments=attachments
    )


if __name__ == '__main__':
    main()
