from analysis import gather

def analyse_sessions(name="report.csv"):
    print("\nAnalysing: Session")
    events = gather.get_events(name)

    sessions = [evt for evt in events if evt.category == "Session" and evt.action == "Time Spent"]

    print("Session Count:", len(sessions))
    by_client = {}
    for session in sessions:
        client_id = session.client_id
        by_client.setdefault(client_id, [])
        by_client[client_id].append(session)

    for key, val in by_client.items():
        session_time = 0
        for s in val:
            if s.label == "(not set)":
                continue
            session_time += int(s.label)
        print(f'{key}: {session_time / 1000} seconds')
