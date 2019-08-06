class Dimension:
    def __init__(self, key, label):
        self.key = key
        self.label = label

class Dimensions:
    Category = Dimension("ga:eventCategory", "Event Category")
    Action = Dimension("ga:eventAction", "Event Action")
    Label = Dimension("ga:eventLabel", "Event Label")
    UserID = Dimension("ga:dimension1", "User ID")
    ClientID = Dimension("ga:dimension2", "Client ID")
    Timestamp = Dimension("ga:dimension3", "Timestamp")

    @staticmethod
    def get_all():
        return [Dimensions.Category, Dimensions.Action, Dimensions.Label, Dimensions.UserID, Dimensions.ClientID, Dimensions.Timestamp]

    @classmethod
    def create(cls):
        return cls(Dimensions.get_all())

    def __init__(self, dimensions):
        self.dimensions = dimensions

    def keys(self):
        return list(map(lambda x: x.key, self.dimensions))

    def labels(self):
        return list(map(lambda x: x.label, self.dimensions))