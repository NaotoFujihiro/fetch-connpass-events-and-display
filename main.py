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


for keyword in keywords_list_for_search:
    main(keyword)
