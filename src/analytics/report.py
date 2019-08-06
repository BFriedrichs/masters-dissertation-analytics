from analytics import Dimensions, Metrics, Event

class Report:
    def __init__(self, google_analytics, view, dimensions=Dimensions.create(), metrics=Metrics.create(), autofetch=False):
        self.analytics = google_analytics
        self.view = view
        self.dimensions = dimensions
        self.metrics = metrics
        self.fetched = False

        self.events = []

        if autofetch:
            self.fetch()

    def fetch(self, startDate='30daysAgo', endDate='today'):
        reports = self.analytics.reports().batchGet(body={'reportRequests': [{
            'viewId': self.view,
            'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
            'metrics': list(map(lambda x: {'expression': x}, self.metrics.keys())),
            'dimensions': list(map(lambda x: {'name': x}, self.dimensions.keys())),
        }]}).execute()
        report = reports['reports'][0]

        self.events = list(map(lambda x: Event({
            **dict(zip(self.dimensions.keys(), x['dimensions'])),
            **dict(zip(self.metrics.keys(), x['metrics'][0]['values'])
        )}), report['data']['rows']))

        self.fetched = True
