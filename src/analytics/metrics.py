class Metrics:
    Sessions = "ga:sessions"
    Value = "ga:eventValue"

    @staticmethod
    def get_all():
        return [Metrics.Sessions, Metrics.Value]
