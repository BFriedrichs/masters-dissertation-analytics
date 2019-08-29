import datetime
import os
import matplotlib.pyplot as plt
import numpy as np
from analysis import gather


def analyse_notifications(name="report.csv", output=None):
    def write_input(filename, data):
        if output is None:
            return
        with open(os.path.join(output, "input", filename), 'w+') as f:
            f.write(f'{data}')

    print("\n\nAnalysing: Notifications\n")
    events = gather.get_events(name)

    notifications = [evt for evt in events if evt.category == "Notification" and evt.action != "Count"]

    print("Notification Count:", len(notifications))

    by_client = {}
    for event in events:
        by_client.setdefault(event.client_id, [])
        by_client[event.client_id].append(event)

    by_client_notif = {}
    for event in notifications:
        client_id = event.client_id
        by_client_notif.setdefault(client_id, [])
        by_client_notif[client_id].append(event)

    # plt.rcdefaults()
    # fig, ax = plt.subplots()

    # # Example data
    # categories = ('Clients', 'Users')
    # data = [len(by_client.keys()), len(by_user.keys())]

    # y_pos = np.arange(len(categories))

    # ax.barh(y_pos, data, align='center')
    # ax.set_yticks(y_pos)
    # ax.set_yticklabels(categories)
    # ax.invert_yaxis()
    # ax.set_xlabel('Count')
    # if output is None:
    #     plt.show()
    # else:
    #     plt.savefig(os.path.join(output, "notifications.png"))

    action_durations_after_notification = []
    action_counts_after_notification = []
    for key, val in by_client.items():
        if key not in by_client_notif or len(by_client_notif[key]) == 0:
            continue
        # print(f'{key}')
        # print(f'* Events: {len(val)}')
        start = None
        curr = None
        action_count = 0
        s = sorted(val, key=lambda x: x.tstamp)
        for evt in s:
            if evt.category == "Notification" and evt.action == "Open":
                if action_count > 1:
                    action_counts_after_notification.append(action_count)
                    action_durations_after_notification.append(curr - start)
                    # print("a", action_count, curr-start)
                action_count = 0

                # print(f'* Opened Notification: {evt}')
                start = curr = evt.tstamp
            elif curr is not None and evt.tstamp - curr < datetime.timedelta(minutes=5):
                curr = evt.tstamp
                action_count += 1
            else:
                if action_count > 1:
                    action_counts_after_notification.append(action_count)
                    action_durations_after_notification.append(curr - start)
                    # print("b", action_count, curr-start)
                start = curr = None
                action_count = 0

    action_durations_after_notification = [x.total_seconds() for x in action_durations_after_notification]
    action_duration_avg = sum(action_durations_after_notification) / len(action_durations_after_notification)
    action_count_avg = sum(action_counts_after_notification) / len(action_counts_after_notification)

    avg_minutes = (action_duration_avg / 60) % 60
    write_input("time_after_notification.txt", round(avg_minutes * 100) / 100)
    write_input('duration_after_notification.txt', ",".join([str(x) for x in action_durations_after_notification]))

