class Dimensions:
    Category = "ga:eventCategory"
    Action = "ga:eventAction"
    Label = "ga:eventLabel"
    UserID = "ga:dimension1"
    ClientID = "ga:dimension2"
    Timestamp = "ga:dimension3"

    @staticmethod
    def get_all():
        return [Dimensions.Category, Dimensions.Action, Dimensions.Label, Dimensions.UserID, Dimensions.ClientID, Dimensions.Timestamp]
