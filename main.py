#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

# ConnpassAPIのリファレンス: https://connpass.com/about/api/
# ConnpassのWebサイトに対するスクレイピングに関する注意事項: https://connpass.com/robots.txt

from pathlib import Path
from glob import glob

import keywords.InputSearchKeywordsFromConsole as Keywords
from utils import auth, fetch, cache, generator, sheet, folder


# ToDo: Alexaのスキルを作成して、ユーザーから音声で検索キーワードを受け取れるようにする
# Connpassで検索したいキーワードを、ユーザーがコンソールから入力
keywords_list_for_search = Keywords.receive_keywords_from_console()

# ToDo: Alexaのスキルを作成して、ユーザーから音声で検索キーワードを受け取れるようにする
# Connpassで検索したい期間を、ユーザーがコンソールから入力
period_list_for_search = Keywords.receive_period_from_console()

# for Debug
print(keywords_list_for_search)
print(period_list_for_search)
print(", ".join(keywords_list_for_search) + ' で検索します。')
print('期間は ' + period_list_for_search[0] + '-' + period_list_for_search[-1] + ' です。')


def main(keyword):
    # Connpassでのキーワード検索を行う
    # 1回のリクエストの検索結果の最大出力データ数は100件である。
    # 「今月のみ検索したい」といった要望を見越して、月ごとに検索をかけるようにする。

    # ToDo:検索期間に今月が含まれているならば、cacheの有無に関わらずhttpリクエストを送り、cacheを更新する。
    # 検索結果をjson形式で保存して、httpリクエストの回数を減らす。
    for ym in period_list_for_search:
        search_start = 1        # 検索の開始位置
        search_count = 100      # 取得件数

        # 検索結果をjson形式で保存して、httpリクエストの回数を減らす。
        while True:
            cache_dir = Path('cache/')

            # 検索結果をjson形式で保存しておくcache
            cache_events_name = keyword + '/' + str(ym) + '/' + str(search_start) + '.json'
            cache_events_file = cache_dir / Path(cache_events_name)

            # 検索結果のうち、検索結果の総件数を保存するためのcacheファイル
            cache_events_num_name = keyword + '/' + 'available' + '.json'
            cache_events_num_file = cache_dir / Path(cache_events_num_name)

            is_cache_events_exists = cache_events_file.exists()
            is_cache_events_num_exists = cache_events_file.exists()

            # Cacheファイルがなければ、Connpass APIにhttpリクエストを飛ばして、 イベント情報を取得する。
            # Cacheファイルがあれば、何もしない
            if not is_cache_events_exists:
                cache.create_cache(cache_events_file)

                print('Connpassで検索を開始します。')
                fetched_events_json = fetch.fetch_search_results_to_cache(keyword, ym, search_start, search_count)

                # 検索結果のイベントリスト
                events_dict = {'events': fetched_events_json['events']}

                # 取得した情報をcacheに保存する
                cache.save_to_cache(cache_events_file, events_dict)

                # 1度目（search_start = 1）の検索時は、検索結果の総件数をキャッシュファイルに保存する。
                if search_start == 1:
                    if not is_cache_events_num_exists:
                        cache.create_cache(cache_events_num_file)

                    # 検索結果の総件数
                    results_available = fetched_events_json['results_available']
                    results_available_dict = {str(ym): results_available}

                    cache.append_dict_to_cache(cache_events_num_file, results_available_dict)

            # １度目（search_start=1）の時は、ループを実行する回数を把握する。
            if search_start == 1:
                if is_cache_events_exists:
                    results_available = cache.get_value_from_cache(cache_events_num_file, str(ym))
                else:
                    results_available = fetched_events_json['results_available']
                fetch_count = results_available // 100

            # 取得件数の最大値は100件なので、検索結果の総件数が100件以上のときに限り、再度httpリクエストを行う。
            if fetch_count == 0:
                print(ym + 'のイベント検索が終了しました。')
                break

            search_start += 100
            fetch_count -= 1

    # headersとevents_list_per_monthとheadersを、スプレッドシートに保存する。
    # APIを呼び出す前に、listに格納する必要がある。
    # headersは先頭行のタイトルを表し、events_list_per_monthがスプレッドシートの各行に保存されるイベント詳細である。
    headers = [
        'ym', 'ID', 'URL', 'タイトル', '主催者', '充足率', '参加者数', '定員', '会場', '開始時刻', '終了時刻', '更新日時'
    ]

    events_list_per_month = []
    for ym in period_list_for_search:
        cache_file_list_path = 'cache/' + keyword + '/' + str(ym) + '/' + '[0-9]*.json'
        cache_file_per_month_list = list(sorted(glob(cache_file_list_path, recursive=True)))

        for cache_file_per_month in cache_file_per_month_list:
            # get_value_from_cache_filesは、['events'][i]['event_id'] の形式となっている
            events_per_month_list = cache.get_value_from_cache(Path(cache_file_per_month), 'events')

            for event in events_per_month_list:
                event_detail_dict = {
                    'ym': event['started_at'][:7],
                    'ID': event['event_id'],
                    'URL': event['event_url'],
                    'タイトル': event['title'],
                    '主催者': event['owner_display_name'],
                    # 定員の充足率を計算（イベントの人気度を定量的に評価）
                    '充足率': generator.calc_rate(event['accepted'], event['limit']),
                    '参加者数': event['accepted'],
                    '定員': event['limit'],
                    '会場': event['place'],
                    '開始時刻': event['started_at'],
                    '終了時刻': event['ended_at'],
                    '更新日時': event['updated_at']
                }
                events_list_per_month.append(event_detail_dict)
                events_list_per_month.sort(key=lambda x: x['開始時刻'])

    num_events_per_month_list = []
    for ym in period_list_for_search:
        num_events_per_month_list.append(cache.get_value_from_cache(cache_events_num_file, str(ym)))

    # スプレッドシートに保存できるように、リストに格納する。
    headers_list_to_post = [headers]
    events_list_to_post = generator.convert_dict_to_list(events_list_per_month, headers)
    num_events_per_month_to_post = [num_events_per_month_list]

    # ToDo: 検索結果の保存先をGoogle Driveから変更する
    # Needed when operating Google Drive and Spreadsheet.
    google_service = {'drive': auth.build_service('drive'), 'sheets': auth.build_service('sheets')}

    print('Authorization complete!')

    # ToDo: 既にスプレッドシートがある場合は、末尾にイベント情報を追加できるようにする。
    # Spreadsheetを新規作成して、spreadsheet_idを取得する。
    spreadsheet_id = sheet.create_sheets(keyword, google_service['sheets'])

    # Folderを新規作成して、folder_idを取得する。
    folder_id = folder.create_folders(keyword, google_service['drive'])

    # Move the file to the new folder
    folder.move_files(google_service['drive'], spreadsheet_id, folder_id)

    # スプレッドシートにタイトルを投入
    sheet.save_batch_data_to_sheets(
        headers_list_to_post, google_service['sheets'], 'A1', spreadsheet_id,
    )

    print('スプレッドシートにイベント情報を投入しています。')
    # スプレッドシートにイベント情報を投入
    sheet.save_batch_data_to_sheets(
        events_list_to_post, google_service['sheets'], 'A2', spreadsheet_id,
    )

    # 月ごとのイベント数を棒グラフで表す
    # num_yms = len(year) * len(month)
    added_sheet_id = sheet.add_sheets(google_service['sheets'], 'graph_axis', spreadsheet_id)

    sheet.save_batch_data_to_sheets(
        [period_list_for_search], google_service['sheets'], 'graph_axis!A1', spreadsheet_id
    )

    sheet.save_batch_data_to_sheets(
        num_events_per_month_to_post, google_service['sheets'], 'graph_axis!A2', spreadsheet_id
    )

    print('イベント数の推移を表したグラフを作成しています。')
    sheet.draw_charts(google_service['sheets'], spreadsheet_id, added_sheet_id)

    print('All the procedure have done!!')


for keyword in keywords_list_for_search:
    main(keyword)
