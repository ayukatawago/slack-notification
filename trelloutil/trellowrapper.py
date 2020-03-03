from datetime import datetime
from trello import TrelloClient


class TrelloWrapper:
    def __init__(self, api_key, token):
        self.client = TrelloClient(api_key=api_key, token=token)

    def get_board(self, board_name):
        for _board in self.client.list_boards():
            if _board.name == board_name:
                return _board
        return None

    def get_lists(self, board_name):
        board = self.get_board(board_name)
        if board is None:
            return None
        return board.list_lists('open')

    def get_cards(self, board_name):
        list_lists = self.get_lists(board_name)
        if list_lists is None:
            return None
        cards = list()
        for _list in list_lists:
            cards.extend(_list.list_cards('open'))
        return cards

    def get_todo_cards(self, board_name):
        today = datetime.now()
        card_lists = self.get_cards(board_name)
        if card_lists is None:
            return None

        cards = list()
        for _card in card_lists:
            if (_card.due_date != ''
                    and _card.due_date.date() <= today.date()
                    and not _card.is_due_complete):
                cards.append(_card)
        return cards
