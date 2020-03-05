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

    def get_lists(self, board_id):
        board = self.client.get_board(board_id)
        if board is None:
            return None
        return board.list_lists('open')

    def get_open_cards(self, list_id):
        target_list = self.client.get_list(list_id)
        if target_list is None:
            return None
        return target_list.list_cards("open")

    def get_todo_cards(self, list_id):
        today = datetime.now()
        card_lists = self.get_open_cards(list_id)
        if card_lists is None:
            return None

        cards = list()
        for _card in card_lists:
            if (_card.due_date != ''
                    and _card.due_date.date() <= today.date()
                    and not _card.is_due_complete):
                cards.append(_card)
        return cards
