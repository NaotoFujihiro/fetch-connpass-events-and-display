#  -*- encoding: utf-8 -*-

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from pathlib import Path

# Authorize Google Drive and Spreadsheet.
sheets_auth = {'scope': 'https://www.googleapis.com/auth/spreadsheets', 'service_name': 'sheets', 'version': 'v4'}
drive_auth  = {'scope': 'https://www.googleapis.com/auth/drive',        'service_name': 'drive',  'version': 'v3'}


def is_creds_available():
    token_path = Path('./credentials/token.json')
    credentials_path = Path('./credentials/credentials.json')

    scopes = sheets_auth['scope'] + ' ' + drive_auth['scope']

    store = file.Storage(token_path)
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(credentials_path, scopes)
        creds = tools.run_flow(flow, store)

    return creds


def build_service(arg_auth):
    if arg_auth == 'sheets':
        auth = sheets_auth
    elif arg_auth == 'drive':
        auth = drive_auth

    creds = is_creds_available()

    auth_service_name = auth['service_name']
    auth_version = auth['version']
    service = discovery.build(auth_service_name, auth_version, http=creds.authorize(Http()))
    return service
