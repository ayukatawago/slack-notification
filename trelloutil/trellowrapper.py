from trello import TrelloClient
from dateutil.relativedelta import relativedelta


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
        labels = card.labels
        if labels is None:
            card.set_due_complete()
        else:
            current_due = card.due_date
            label_list = [label.name for label in labels]
            if "daily" in label_list:
                next_due = current_due + relativedelta(days=1)
            elif "weekly" in label_list:
                next_due = current_due + relativedelta(weeks=1)
            elif "monthly" in label_list:
                next_due = current_due + relativedelta(months=1)
            elif "yearly" in label_list:
                next_due = current_due + relativedelta(years=1)
            else:
                return
            card.set_due(next_due)

    def postpone_card(self, card_id):
        card = self.get_card(card_id)
        current_due = card.due_date
        next_due = current_due + relativedelta(days=1)
        card.set_due(next_due)
