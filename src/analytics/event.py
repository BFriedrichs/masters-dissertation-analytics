import datetime
from analytics import Dimensions, Metrics

class Event:
    def __init__(self, dict_rep):
        self.category = dict_rep[Dimensions.Category.key]
        self.action = dict_rep[Dimensions.Action.key]
        self.label = dict_rep[Dimensions.Label.key]
        self.value = dict_rep[Metrics.Value.key]
        self.user_id = dict_rep[Dimensions.UserID.key]
        self.client_id = dict_rep[Dimensions.ClientID.key]
        self.orig_tstamp = int(dict_rep[Dimensions.Timestamp.key])
        self.tstamp = datetime.datetime.fromtimestamp(self.orig_tstamp / 1000)

    def __repr__(self):
        return f'<Event category="{self.category}" action="{self.action}" label="{self.label}">'

    def as_list(self):
        return [self.category, self.action, self.label, self.value, self.user_id, self.client_id, self.orig_tstamp]

    @staticmethod
    def list_headers():
        return [Dimensions.Category, Dimensions.Action, Dimensions.Label, Metrics.Value, Dimensions.UserID, Dimensions.ClientID, Dimensions.Timestamp]