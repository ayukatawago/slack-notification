from datetime import datetime
from slackutil.slackbuilder import SlackBlockBuilder, SlackAttachmentBuilder, SlackElementsBuilder
from slackutil.slackwrapper import SlackApiWrapper
from trelloutil.trellowrapper import TrelloApiWrapper
import config


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
        due_date = card.due_date.astimezone().strftime("%Y/%m/%d")

        elements = SlackElementsBuilder()
        elements.add_button("complete", card.id, "primary")
        elements.add_button("postpone", card.id)

        item = SlackBlockBuilder()
        item.add_section(task_name)
        item.add_context(due_date)
        item.add_actions(elements.build())

        if card.due_date.astimezone().date() < today.date():
            color = "#ff9900"
        else:
            color = "#00c300"
        builder.add_item(item.build(), color)
    return builder.build()


def get_todo_cards(trello_list):
    today = datetime.now()
    trello_cards = list()
    open_cards = trello_list.list_cards("open")
    if len(open_cards) == 0:
        return trello_cards

    for card in open_cards:
        if (card.due_date != ''
                and card.due_date.date() <= today.date()
                and not card.is_due_complete):
            trello_cards.append(card)
    return trello_cards


def notify_trello_tasks():
    slack = SlackApiWrapper(config.slack_api_token)
    # get cards from Trello
    trello = TrelloApiWrapper(config.trello_api_key, config.trello_token)
    trello_board = trello.get_board_by_name(config.trello_board)
    open_lists = trello_board.list_lists("open")
    for trello_list in open_lists:
        trello_cards = get_todo_cards(trello_list)
        if len(trello_cards) == 0:
            continue

        # notify to slack
        blocks = create_trello_block(trello_list.name)
        attachments = create_trello_attachments(trello_cards)
        slack.post_attachment_message(
            channel=config.slack_trello_channel,
            blocks=blocks,
            attachments=attachments
        )