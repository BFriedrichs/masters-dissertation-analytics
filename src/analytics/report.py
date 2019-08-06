from analytics import Dimensions, Metrics, Event

class Report:
    def __init__(self, google_analytics, view, dimensions=Dimensions.get_all(), metrics=Metrics.get_all(), autofetch=False):
        self.analytics = google_analytics
        self.view = view
        self.dimensions = dimensions
        self.metrics = metrics
        self.fetched = False

        self.data = []

        if autofetch:
            self.fetch()

    def fetch(self, startDate='30daysAgo', endDate='today'):
        reports = self.analytics.reports().batchGet(body={'reportRequests': [{
            'viewId': self.view,
            'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
            'metrics': list(map(lambda x: {'expression': x}, self.metrics)),
            'dimensions': list(map(lambda x: {'name': x}, self.dimensions)),
        }]}).execute()
        report = reports['reports'][0]

        self.data = list(map(lambda x: Event({
            **dict(zip(self.dimensions, x['dimensions'])),
            **dict(zip(self.metrics, x['metrics'][0]['values'])),
        }), report['data']['rows']))

        self.fetched = True
