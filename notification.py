from datetime import datetime
from trelloutil.trellowrapper import TrelloWrapper
from slackutil.slackbot import SlackBot
from slackutil.slackbuilder import SlackBlockBuilder, SlackAttachmentBuilder
import config


slack = SlackBot(config.slack_api_token)


def create_trello_block(list_name):
    block = SlackBlockBuilder()
    block.add_section("*Today's task in `{}`*".format(list_name))
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


def notify_trello_tasks():
    # get cards from Trello
    trello = TrelloWrapper(config.trello_api_key, config.trello_token)
    trello_board = trello.get_board(config.trello_board)
    trello_lists = trello.get_lists(trello_board.id)
    for trello_list in trello_lists:
        trello_cards = trello.get_todo_cards(trello_list.id)
        if len(trello_cards) == 0:
            continue

        # notify to slack
        blocks = create_trello_block(trello_list.name)
        attachments = create_trello_attachments(trello_cards)
        slack.post_attachment_message(
            channel=config.slack_channel,
            blocks=blocks,
            attachments=attachments
        )


if __name__ == '__main__':
    notify_trello_tasks()
