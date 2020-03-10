from trello import TrelloClient
from datetime import timedelta

class TrelloApiWrapper(TrelloClient):
    def __init__(self, api_key, token):
        super().__init__(api_key, token)

    def get_board_by_name(self, board_name):
        for _board in self.list_boards():
            if _board.name == board_name:
                return _board
        return None

    def complete_card(self, card_id):
        card = self.get_card(card_id)
        card.set_due_complete()

    def postpone_card(self, card_id):
        card = self.get_card(card_id)
        current_due = card.due_date
        next_due = current_due + timedelta(days=1)
        card.set_due(next_due)
