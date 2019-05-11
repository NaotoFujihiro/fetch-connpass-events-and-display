#  -*- encoding: utf-8 -*-


def create_sheets(keyword, sheets_service):
    body = {
        'properties': {
            'title': keyword
        }
    }
    new_sheet = sheets_service.spreadsheets().create(
        body=body,
        fields='spreadsheetId'
    ).execute()
    spreadsheet_id = new_sheet.get('spreadsheetId')
    return spreadsheet_id


# range_でsheet_idを指定できる
def save_batch_data_to_sheets(batch_data, sheets_service, range_, id_):
    body = {
        'valueInputOption': 'RAW',
        'data': [
            {
                'range': range_,
                'majorDimension': 'ROWS',
                'values': batch_data
            }
        ]
    }

    res = sheets_service.spreadsheets().values().batchUpdate(
        spreadsheetId=id_,
        body=body
    ).execute()

    return res


def add_sheets(sheets_service, title, id_):
    requests = [
        {
            "addSheet": {
                "properties": {
                    "title": title,
                    "tabColor": {
                        "red": 1.0,
                        "green": 0.3,
                        "blue": 0.4
                    }
                }
            }
        }
    ]

    add_sheets_body = {'requests': requests}
    added_sheet = sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=id_,
        body=add_sheets_body
    ).execute()

    # sheet_idはスプレッドシートURLの'gid=sheet_id'の=以下
    added_sheet_id = added_sheet['replies'][0]['addSheet']['properties']['sheetId']
    return added_sheet_id


def draw_charts(sheets_service, spreadsheet_id, sheet_id):
    requests = [
        {
            'addChart': {
                'chart': {
                    'spec': {
                        'title': 'Transition of the Number of Events',
                        'basicChart': {
                            'chartType': 'COLUMN',
                            'legendPosition': 'BOTTOM_LEGEND',
                            'axis': [
                                {
                                    'position': 'BOTTOM_AXIS',
                                    'title': 'yyyy/mm'
                                },
                                {
                                    'position': 'LEFT_AXIS',
                                    'title': 'The Number of the Events'
                                }
                            ],
                            'domains': [
                                {
                                    'domain': {
                                        'sourceRange': {
                                            'sources': [
                                                {
                                                    'sheetId': sheet_id,
                                                    'startRowIndex': 0,
                                                    'endRowIndex': 1,
                                                    'startColumnIndex': 0
                                                    # 'endColumnIndex': 1
                                                }
                                            ]
                                        }
                                    }
                                }
                            ],
                            'series': [
                                {
                                    'series': {
                                        'sourceRange': {
                                            'sources': [
                                                {
                                                    'sheetId': sheet_id,
                                                    'startRowIndex': 1,
                                                    'endRowIndex': 2,
                                                    'startColumnIndex': 0
                                                    # 'endColumnIndex': 1
                                                }
                                            ]
                                        }
                                    },
                                    'targetAxis': 'LEFT_AXIS'
                                }
                            ],
                            'headerCount': 1
                        }
                    },
                    'position': {
                        'newSheet': True
                    }
                }
            }
        }
    ]

    draw_chart_body = {'requests': requests}
    request = sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=draw_chart_body
    )

    return request.execute()
