#  -*- encoding: utf-8 -*-

import requests
import json
from time import sleep
import sys


def fetch_search_results_to_cache(keyword, ym, search_start, search_count, timeout=100):
    fetch_url = 'https://connpass.com/api/v1/event/'
    # スクレイピングの間隔を設定: https://connpass.com/robots.txt
    crawl_delay_sec = 5

    # robots.txt に従っていないときは、強制的にスクレイピングを終了
    if crawl_delay_sec > 5:
        print('スクレイピングのhttpリクエストの間隔を見直してください。\n')
        print('プログラムを終了します。')
        sys.exit()

    payload = {
        'keyword':      keyword,        # keyword: キーワード (AND), AND条件部分一致。複数指定可能。
        'keyword_or':   keyword,        # keyword_or: キーワード (OR), OR条件部分一致。複数指定可能。
        'ym':           ym,             # イベント開催年月
        'start':        search_start,   # 検索の開始位置
        'order':        2,              # 検索結果の表示順、2:開催日時順
        'count':        search_count,   # 取得件数
    }

    fetch_trial_count = 0
    while fetch_trial_count < 10:
        try:
            print('-----\n' + str(ym))
            print('-----\n' + str(search_start))
            print('-----\n' + str(fetch_trial_count+1) + '回目')
            fetched_search_results = requests.get(fetch_url, timeout=timeout, params=payload)

            fetched_search_results_json = fetched_search_results.json()
            return fetched_search_results_json
        except json.decoder.JSONDecodeError as ex:
            print(ex)

        sleep(crawl_delay_sec)
        fetch_trial_count += 1

    return None
