import datetime
from analytics import Dimensions, Metrics

class Event:
    def __init__(self, dict_rep):
        self.category = dict_rep[Dimensions.Category]
        self.action = dict_rep[Dimensions.Action]
        self.label = dict_rep[Dimensions.Label]
        self.value = dict_rep[Metrics.Value]
        self.user_id = dict_rep[Dimensions.UserID]
        self.client_id = dict_rep[Dimensions.ClientID]
        self.tstamp = datetime.datetime.fromtimestamp(int(dict_rep[Dimensions.Timestamp]) / 1000)

    def __repr__(self):
        return f'<Event category="{self.category}" action="{self.action}" label="{self.label}" >'
