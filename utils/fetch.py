#  -*- encoding: utf-8 -*-

import requests
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
        print('-----\n' + str(ym))
        print('-----\n' + str(search_start))
        print('-----\n' + str(fetch_trial_count+1) + '回目')
        response = requests.get(fetch_url, timeout=timeout, params=payload)

        # HTTPステータスコードが200番代の場合、raise_for_status()メソッドは'NoneType'型となる
        is_request_success = response.raise_for_status() is None
        is_content_json = response.headers['Content-Type'] == 'text/json; charset=utf-8'

        if is_request_success and is_content_json:
            print('HTTP status code is: ' + str(response.status_code))
            print(response.headers['Content-Type'] + '形式でデータを取得しました。')
            return response.json()
        else:
            print(response.raise_for_status())
            print('JSON形式でデータを取得できなかったので、再度リクエストしています。')
            sleep(crawl_delay_sec)
            fetch_trial_count += 1
            continue

    return None
