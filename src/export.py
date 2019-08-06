import os
import csv
from analytics import Dimensions, Metrics, Event

CSV_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'csv')

def export_report_csv(report, name="report.csv", anonymous=False):
    os.makedirs(CSV_FOLDER, exist_ok=True)
    with open(os.path.join(CSV_FOLDER, name), 'w+') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(Event.list_headers())

        events = report.events
        if anonymous:
            client_id_dict = {x.client_id: x for x in events }
            user_id_dict = {x.user_id: x for x in events if x.user_id != "None"}

            cid_counter = 0
            cid_map = {}
            uid_counter = 0
            uid_map = {}
            for event in events:
                if event.client_id in client_id_dict:
                    curr_id = cid_map.get(event.client_id, None)
                    if curr_id is None:
                        curr_id = cid_map[event.client_id] = cid_counter
                        cid_counter += 1
                    event.client_id = f'CLIENT_{curr_id}'

                if event.user_id in user_id_dict:
                    curr_id = uid_map.get(event.user_id, None)
                    if curr_id is None:
                        curr_id = uid_map[event.user_id] = uid_counter
                        uid_counter += 1
                    event.user_id = f'USER_{curr_id}'


        csvwriter.writerows([evt.as_list() for evt in events])
