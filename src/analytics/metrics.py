class Metric:
    def __init__(self, key, label):
        self.key = key
        self.label = label

class Metrics:
    Sessions = Metric("ga:sessions", "Sessions")
    Value = Metric("ga:eventValue", "Event Value")
    TotalEvents = Metric("ga:totalEvents", "Total Events")
    UniqueEvents = Metric("ga:uniqueEvents", "Unique Events")

    @staticmethod
    def get_all():
        return [Metrics.Sessions, Metrics.Value, Metrics.TotalEvents, Metrics.UniqueEvents]

    @classmethod
    def create(cls):
        return cls(Metrics.get_all())

    def __init__(self, metrics):
        self.metrics = metrics

    def keys(self):
        return list(map(lambda x: x.key, self.metrics))

    def labels(self):
        return list(map(lambda x: x.label, self.metrics))
