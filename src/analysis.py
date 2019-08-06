import os
import csv

from analytics import Event

CSV_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'csv')

def get_events(name):
    with open(os.path.join(CSV_FOLDER, name), 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader, None)

        list_headers = list(map(lambda x: x.key, Event.list_headers()))
        return [Event(dict(zip(list_headers, row))) for row in reader]

def analyse_notifications(name="report.csv"):
    events = get_events(name)
    notifications = [evt for evt in events if evt.category == "Notification" and evt.action == "Open"]
    print(notifications)
