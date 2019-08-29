import datetime
from analytics import Dimensions, Metrics

def clean_rep(data):
    if data is None or data == "None" or data == "(not set)" or data == "":
        return None
    return data

class Event:
    def __init__(self, dict_rep):
        self.category = clean_rep(dict_rep[Dimensions.Category.key])
        self.action = clean_rep(dict_rep[Dimensions.Action.key])
        self.label = clean_rep(dict_rep[Dimensions.Label.key])
        self.value = clean_rep(dict_rep[Metrics.Value.key])
        self.client_id = dict_rep[Dimensions.ClientID.key]
        self.orig_tstamp = int(dict_rep[Dimensions.Timestamp.key])
        self.tstamp = datetime.datetime.fromtimestamp(self.orig_tstamp / 1000)
        self.continent = clean_rep(dict_rep[Dimensions.Continent.key])
        self.country = clean_rep(dict_rep[Dimensions.Country.key])
        self.total_events = clean_rep(dict_rep[Metrics.TotalEvents.key])
        self.operating_system = clean_rep(dict_rep[Dimensions.OS.key])
        self.user_id = clean_rep(dict_rep[Dimensions.UserID.key])

    def __repr__(self):
        return f'<Event category="{self.category}" action="{self.action}" label="{self.label}">'

    def as_list(self):
        return [self.category, self.action, self.label, self.value, self.user_id, self.client_id, self.orig_tstamp, self.continent, self.country, self.operating_system, self.total_events]

    @staticmethod
    def list_headers():
        return [Dimensions.Category, Dimensions.Action, Dimensions.Label, Metrics.Value, Dimensions.UserID, Dimensions.ClientID, Dimensions.Timestamp, Dimensions.Continent, Dimensions.Country, Dimensions.OS, Metrics.TotalEvents]