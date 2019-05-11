#  -*- encoding: utf-8 -*-

import json


def create_cache(cache):
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.touch()

    return 0


def save_to_cache(cache, dict_to_save):
    with cache.open(mode='w') as file:
        json.dump(dict_to_save, file)

    return 0


def append_dict_to_cache(cache, dict_to_append):
    try:
        with cache.open(mode='r') as file:
            cache_dict = json.load(file)
    except json.decoder.JSONDecodeError:
        cache_dict = {}

    dict_key = list(dict_to_append.keys())[0]
    print(dict_key)
    cache_dict[dict_key] = dict_to_append[dict_key]

    with open(cache, mode='w') as file:
        json.dump(cache_dict, file)

    return 0


def get_value_from_cache(cache, key):
    with cache.open(mode='r') as file:
        file_dict = json.load(file)
        return file_dict[key]
