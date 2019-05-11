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

def main(keyword):
    # Connpassでのキーワード検索を行う
    # 1回のリクエストの検索結果の最大出力データ数は100件である。
    # 「今月のみ検索したい」といった要望を見越して、月ごとに検索をかけるようにする。

    # ToDo: 検索結果の保存先をGoogle Driveから変更する
    # Needed when operating Google Drive and Spreadsheet.
    google_service = {'drive': auth.build_service('drive'), 'sheets': auth.build_service('sheets')}

    print('Authorization complete!')


for keyword in keywords_list_for_search:
    main(keyword)
