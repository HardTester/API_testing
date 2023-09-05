def remove_ids(origin_dict):
    """
    Удаляет ключи из словаря, в которых есть id или Id
    :param origin_dict: исходный словарь
    :return: словарь с выпиленными айдишниками
    """

    def rmv_ids(d):
        keys_to_remove = []

        for key, value in d.items():
            if isinstance(value, dict):
                rmv_ids(value)
            elif isinstance(value, list):
                for val in value:
                    rmv_ids(val)
            elif 'id' in key or 'Id' in key:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del d[key]

    res = origin_dict.copy()
    rmv_ids(res)
    return res


def compare_json_left_in_right(json1, json2, key=None, path=''):
    """
    лишние ключи из левого json - игнорируются
    несовпание по типу -> значения левого и правого ключей
    отсутствие ключа в правом json -> значения левого и правого None
    несовпание по значению -> значения левого и правого ключей
    """
    diff_dict = {}
    if isinstance(json1, dict) and isinstance(json2, dict):
        for key in json1:
            if key not in json2:
                diff_dict[key] = (json1[key], "key undefined", f"{path}{key}")
                continue
            diff_dict.update(compare_json_left_in_right(json1[key], json2[key], key, f"{path}{key}:"))
    elif json1 != json2:
        diff_dict[key] = (json1, json2, path[:-1])
    return diff_dict
