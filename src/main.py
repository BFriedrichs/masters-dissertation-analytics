import os
import json
from apiclient.discovery import build
from google.oauth2 import service_account

from analytics import Report

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'creds.json')
CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.json')

if __name__ == "__main__":
    config = {}
    with open(CONFIG_FILE, 'r') as fp:
        config = json.load(fp)

    credentials = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)

    # Build the service object.
    google_analytics = build('analyticsreporting', 'v4', credentials=credentials)
    report = Report(google_analytics, view=config['view_id'])
    report.fetch()
    print(report.data)
