from trello import TrelloClient


class TrelloApiWrapper(TrelloClient):
    def __init__(self, api_key, token):
        super().__init__(api_key, token)

    def get_board(self, board_name):
        for _board in self.list_boards():
            if _board.name == board_name:
                return _board
        return None

    def complete_card(self, card_id):
        card = self.get_card(card_id)
        card.set_due_complete()
