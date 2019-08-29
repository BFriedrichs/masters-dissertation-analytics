import os
import matplotlib.pyplot as plt
import numpy as np
import datetime
from scipy import signal, stats
from analysis import gather, statistics

def to_timedelta(date):
    return datetime.timedelta(hours=date.hour, minutes=date.minute, seconds=date.second)

def pretty_hour(hour, short=False):
    curr_hr = str(hour)
    if len(str(curr_hr)) == 1:
        curr_hr = f'0{curr_hr}'
    if not short:
        curr_hr = f'{curr_hr}:00'
    return curr_hr

def pretty_time(seconds):
    hr = pretty_hour(int(seconds // 3600), short=True)
    mn = pretty_hour(int((seconds // 60) % 60), short=True)
    return f'{hr}:{mn}'

def analyse_frequency(name="report.csv", output=None):
    def write_input(filename, data):
        if output is None:
            return
        with open(os.path.join(output, "input", filename), 'w+') as f:
            f.write(f'{data}')

    print("\nGenerating: Frequency\n")
    events = gather.get_events(name)

    notifications = []
    sessions = []
    session_times = []
    by_client = {}
    by_continent = {}
    by_system = {}

    daily_session = {}
    daily_notifications = {}
    daily_client_notifications = {}
    daily_client_notifications_open = {}

    time_of_day_sessions = []
    time_of_day_notifications = []

    client_systems = {}
    client_continents = {}
    client_notifications_received = {
        "Received": [],
        "None received": []
    }
    client_notifications_opened = {
        "Opened": [],
        "None opened": []
    }
    users = {"Registered": [], "Unregistered": []}

    for evt in events:
        unique_day = f'{evt.tstamp.year}:{evt.tstamp.month}:{evt.tstamp.day}'

        if evt.category == "Notification" and evt.action != "Count":
            notifications.append(evt)
            if evt.action == "Received":
                time_of_day_notifications.append(to_timedelta(evt.tstamp).total_seconds())
                daily_notifications.setdefault(unique_day, [])
                daily_notifications[unique_day].append(evt)

                daily_client_notifications.setdefault(unique_day, {})
                daily_client_notifications[unique_day].setdefault(evt.client_id, [])
                daily_client_notifications[unique_day][evt.client_id].append(evt)
            elif evt.action == "Open":
                daily_client_notifications_open.setdefault(unique_day, {})
                daily_client_notifications_open[unique_day].setdefault(evt.client_id, [])
                daily_client_notifications_open[unique_day][evt.client_id].append(evt)
        elif evt.category == "Session":
            if evt.label is not None:
                spent = int(evt.label)
                if spent > 1000:
                    sessions.append(evt)
                    session_times.append(spent)
            time_of_day_sessions.append(to_timedelta(evt.tstamp).total_seconds())
            daily_session.setdefault(unique_day, [])
            daily_session[unique_day].append(evt)
        by_client.setdefault(evt.client_id, [])
        by_client[evt.client_id].append(evt)

        by_system.setdefault(evt.operating_system, [])
        by_system[evt.operating_system].append(evt)

        by_continent.setdefault(evt.continent, [])
        by_continent[evt.continent].append(evt)

    received_clients = {}
    for cid, evts in by_client.items():
        user_id = None
        opened = False
        received = False
        for evt in evts:
            if evt.category == "Notification":
                if evt.action == "Received":
                    received = True
                elif evt.action == "Open":
                    opened = True
            if evt.user_id is not None:
                user_id = evt.user_id
            if received and user_id and opened:
                break
        if received or opened:
            received_clients[cid] = 1

        receive_key = "Received" if received else "None received"
        client_notifications_received[receive_key].append(1)

        open_key = "Opened" if received else "None opened"
        client_notifications_opened[open_key].append(1)

        evt = evts[0]
        client_continents.setdefault(evt.continent, [])
        client_continents[evt.continent].append(1)

        client_systems.setdefault(evt.operating_system, [])
        client_systems[evt.operating_system].append(1)

        if user_id is None:
            users["Unregistered"].append(1)
        else:
            users["Registered"].append(1)

    plt.rcdefaults()
    fig, ax = plt.subplots()

    categories = ['Users', 'Continents', 'Systems', 'Received', 'Opened']
    bars = [users, client_continents, client_systems, client_notifications_received, client_notifications_opened]
    entries = [list(zip(x.keys(), [len(evts) for evts in x.values()])) for x in bars]

    for y, (category, data) in enumerate(zip(categories, entries)):
        category_colors = plt.get_cmap('RdYlGn')(
            np.linspace(0.15, 0.85, len(data)))
        widths = np.array([entry[1] for entry in data]) * (1 / len(by_client.keys()))
        starts = [0, *widths.cumsum()[:-1]]

        ax.barh(category, widths, left=starts, height=0.5, label=category, color=category_colors)

        centers = starts + widths / 2
        for yy, (center, width, entry) in enumerate(zip(centers, widths, data)):
            color = category_colors[yy]
            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            ax.text(center, y, f'{entry[0]} ({entry[1]})', ha='center', va='center', color=text_color, bbox=dict(fc=color, ec='none', alpha=0.9))

    ax.invert_yaxis()
    # ax.xaxis.set_visible(False)
    # ax.barh(y_pos, nums, align='center')
    # ax.set_yticks(y_pos)
    # ax.set_yticklabels(names)
    # ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Unique clients')
    steps = 5
    ax.set_xticks(np.linspace(0, 1, steps))
    ax.set_xticklabels(np.linspace(0, len(by_client.keys()), steps, dtype=int))

    if output is None:
        plt.show()
    else:
        plt.savefig(os.path.join(output, "plots", "frequency.png"))

    plt.rcdefaults()
    fig, ax = plt.subplots()

    time_data = [time_of_day_sessions, time_of_day_notifications]
    bp = ax.violinplot(time_data)

    hour_range = 25
    y_ticks_by_hour = [datetime.timedelta(hours=x).total_seconds() for x in range(hour_range)]
    ax.set_yticks(y_ticks_by_hour)
    ax.set_yticklabels([pretty_hour(x) for x in range(hour_range)])
    ax.set_xticks([1, 2])
    ax.set_xticklabels(["Sessions", "Notifications"])

    def avg_group(n, step):
        ret = [[] for _ in range(25)]
        for nn in n:
            i = int(round(nn // step / 2))
            ret[i].append(nn)
        return ret

    grouped_time_of_day_sessions = avg_group(time_of_day_sessions, 1800)
    grouped_time_of_day_notifications = avg_group(time_of_day_notifications, 1800)

    f1 = []
    f2 = []
    for i in range(len(grouped_time_of_day_notifications)):
        if len(grouped_time_of_day_notifications[i]) == 0:
            continue
        f1.append(len(grouped_time_of_day_sessions[i]))
        f2.append(len(grouped_time_of_day_notifications[i]))
    a = stats.pearsonr(f1, f2)
    # DO SOMETHING WITH THIS

    if output is None:
        plt.show()
    else:
        plt.savefig(os.path.join(output, "plots", "times.png"))

    plt.rcdefaults()
    fig, ax = plt.subplots()

    bp = ax.boxplot(time_data)
    common_time_of_day = [w for w in bp['whiskers']]
    common_session = [w.get_ydata() for w in common_time_of_day[0:2]]
    common_notifications = [w.get_ydata() for w in common_time_of_day[2:4]]

    write_input('session_time_min.txt', pretty_time(min(time_of_day_sessions)))
    write_input('session_time_max.txt', pretty_time(max(time_of_day_sessions)))
    write_input('common_session_time_min.txt', pretty_time(common_session[0][0]))
    write_input('common_session_time_max.txt', pretty_time(common_session[1][0]))

    write_input('client_count.txt', len(by_client.keys()))
    write_input('user_count.txt', len(users["Registered"]))
    write_input('action_count.txt', len(events))

    write_input('continent_european_count.txt', len(client_continents['Europe']))
    write_input('continent_us_count.txt', len(client_continents['Americas']))
    other_continent_count = sum(len(v) for k,v in client_continents.items() if k != "Europe" and k != "Americas")
    write_input('continent_other_count.txt', other_continent_count)

    write_input('session_times.txt', ",".join([str(x / 1000) for x in session_times]))
    write_input('session_minutes_avg.txt', round(sum(session_times) / len(sessions) / 1000 / 60, 2))
    write_input('session_minutes_max.txt', round(max(session_times) / 1000 / 60, 2))
    write_input('session_minutes_min.txt', round(min(session_times) / 1000 / 60, 2))

    received = []
    opened = []
    clients = {}

    for notif in notifications:
        if notif.action == "Open":
            opened.append(notif)
        elif notif.action == "Received":
            received.append(notif)
        clients[notif.client_id] = 1

    write_input('notification_received_count.txt', len(received))
    write_input('notification_opened_count.txt', len(opened))

    daily_notification_counts = [len(value) for key, value in daily_notifications.items() if len(value) < 100]
    daily_notification_sum = sum(daily_notification_counts)
    write_input('daily_notification_count_avg.txt', daily_notification_sum / len(daily_notification_counts))

    # daily_client_counts = [len(evts.values()) for evts in 
    daily_per_user_averages = [sum([len(c_evt) for c_evt in days.values()]) / len(days) for days in daily_client_notifications.values()]
    write_input('daily_notification_count_avg_per_user.txt', round(sum(daily_per_user_averages) / len(daily_per_user_averages) * 100) / 100)

    daily_per_notification_max = [max([len(c_evt) for c_evt in days.values()]) for days in daily_client_notifications.values()]
    write_input('daily_notification_count_max.txt', max(daily_per_notification_max))

    daily_per_user_averages_open = [sum([len(c_evt) for c_evt in days.values()]) / len(days) for days in daily_client_notifications_open.values()]
    write_input('daily_notification_count_open_avg_per_user.txt', round(sum(daily_per_user_averages_open) / len(daily_per_user_averages_open) * 100) / 100)


    notification_sessions = {}
    non_notification_sessions = {}
    for key, sessions_of_day in daily_session.items():
        for session in sessions_of_day:
            if session.client_id in received_clients:
                notification_sessions.setdefault(key, [])
                notification_sessions[key].append(session)
            else:
                non_notification_sessions.setdefault(key, [])
                non_notification_sessions[key].append(session)

    sessions_per_day = [len(x) for x in daily_session.values()]
    avg_sessions_per_day = sum(sessions_per_day) / len(daily_session.values())
    write_input('sessions_per_day_avg.txt', round(avg_sessions_per_day))
    write_input('sessions_per_day_max.txt', max(sessions_per_day))

    notification_sessions_per_day = [len(x) for x in notification_sessions.values() if len(x) < 40]
    avg_notification_sessions = sum(notification_sessions_per_day) / len(notification_sessions.values())
    write_input('notification_sessions_per_day_avg.txt', round(avg_notification_sessions))
    write_input('notification_sessions_per_day_max.txt', max(notification_sessions_per_day))

    non_notification_sessions_per_day = [len(x) for x in non_notification_sessions.values() if len(x) < 40]
    avg_non_notification_sessions = sum(non_notification_sessions_per_day) / len(non_notification_sessions.values())
    write_input('non_notification_sessions_per_day_avg.txt', round(avg_non_notification_sessions))
    write_input('non_notification_sessions_per_day_max.txt', max(non_notification_sessions_per_day))

    notification_sessions_per_hour = [[] for _ in range(25)]
    non_notification_sessions_per_hour = [[] for _ in range(25)]

    for cid, evts in by_client.items():
        for evt in evts:
            if evt.category != "Session" or evt.label == None:
                continue
            seconds = to_timedelta(evt.tstamp).total_seconds()
            i = int(round(seconds // 1800 / 2))

            spent = int(evt.label) / 1000
            if spent > 250:
                continue
            if cid in received_clients:
                notification_sessions_per_hour[i].append(spent)
            else:
                non_notification_sessions_per_hour[i].append(spent)

    plt.close()
    plt.close()
    plt.close()
    plt.close()
    plt.rcdefaults()
    fig, ax = plt.subplots()

    def time_ranged(arr):
        return list(arr[8:18])

    ax.set_ylabel('Average session length')
    ax.set_xticks(range(18-8))
    ax.set_xticklabels(time_ranged([pretty_hour(x) for x in range(hour_range)]))

    notification_per_hour_means = [int(np.mean(x)) if len(x) > 0 else 0 for x in notification_sessions_per_hour]
    non_notification_per_hour_means = [int(np.mean(x)) if len(x) > 0 else 0 for x in non_notification_sessions_per_hour]

    width = 0.35
    ind = np.arange(len(time_ranged(notification_per_hour_means)))
    ax.bar(ind - width/2, time_ranged(notification_per_hour_means), width, label='with')
    ax.bar(ind + width/2, time_ranged(non_notification_per_hour_means), width, label='without')

    if output is None:
        plt.show()
    else:
        plt.savefig(os.path.join(output, "plots", "session_length_by_hour.png"))

    plt.close()
