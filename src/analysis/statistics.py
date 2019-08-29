import os
from scipy import stats

CSV_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'csv')

def generate_all(output=None):
    def get_fd(name):
        return open(os.path.join(output, 'input', name), 'r')
    def write_input(filename, data):
        if output is None:
            return
        with open(os.path.join(output, "input", filename), 'w+') as f:
            f.write(f'{data}')

    generate_avg_to_notification_session(get_fd, write_input)

def generate_avg_to_notification_session(get_fd, write_input):
    fd_notification = get_fd('duration_after_notification.txt')
    fd_avg = get_fd('session_times.txt')

    session_times = [float(x) for x in fd_avg.read().split(",")]
    after_notification_times = [float(x) for x in fd_notification.read().split(",")]

    ana = stats.mannwhitneyu(session_times, after_notification_times)
    write_input('pvalue_time_session_vs_notification.txt', round(ana.pvalue * 1000) / 1000)

    fd_notification.close()
    fd_avg.close()