import re


def receive_keywords_from_console():
    display_message = 'Connpassで検索したいキーワードを入力してください。\nコンマ区切りで複数入力できます。\n入力キーワード: '
    return list(keyword.strip() for keyword in input(display_message).split(','))


def receive_period_from_console():
    message = 'イベントを検索する期間を指定してください。'
    print(message)

    message_begin = '何年何月から検索しますか？ (ex. 2012-01): '
    message_end = '何年何月まで検索しますか？ (ex. 2019-04): '

    while True:
        input_period_begin_in = input(message_begin)
        if (len(input_period_begin_in) == 7) and (re.match('201[0-9]{1}-[0-1]{1}[0-9]{1}', input_period_begin_in)):
            input_period_list_begin_in = list(input_period_begin_in.split('-'))
            break
        else:
            print('\"2012-01\" という形式で入力してください。')

    while True:
        input_period_end_in = input(message_end)
        if len(input_period_end_in) == 7:
            input_period_list_end_in = list(input_period_end_in.split('-'))
            break
        else:
            print('\"2019-04\" という形式で入力してください。')

    return generate_month_and_year_between_period(input_period_list_begin_in, input_period_list_end_in)


def generate_month_and_year_between_period(period_begin_in, period_end_in):
    year_begin_in = int(period_begin_in[0])
    month_begin_in = int(period_begin_in[1])

    year_end_in = int(period_end_in[0])
    month_end_in = int(period_end_in[1])

    num_of_month_between_period = (year_end_in - year_begin_in) * 12 + (month_end_in - month_begin_in + 1)

    ym = []
    for i in range(num_of_month_between_period):
        if (month_begin_in + i) % 12 != 0:
            month_i = (month_begin_in + i) % 12
            year_i = year_begin_in + ((month_begin_in + i) // 12)
        else:
            month_i = 12
            year_i = year_begin_in + ((month_begin_in + i) // 12) -1

        ym.append(str(year_i) + str(format(month_i, '02')))

    return ym
