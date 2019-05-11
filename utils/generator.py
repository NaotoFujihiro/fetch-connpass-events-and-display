def calc_rate(denominator, numerator):
    # 分母の例外処理
    if isinstance(numerator, type(None)) is True or numerator == 0:
        return 0
    else:
        return (denominator / numerator) * 100


def convert_dict_to_list(dict_in_list, key_list):
    converted_list = []
    for dict_ in dict_in_list:
        converted_list_per_dict = []
        for key in key_list:
            converted_list_per_dict.append(dict_[key])
        converted_list.append(converted_list_per_dict)
    return converted_list
