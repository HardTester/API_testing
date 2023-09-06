def remove_ids(origin_dict):
    """
    Удаляет ключи из словаря, в которых есть id
    :param origin_dict: исходный словарь
    :return: словарь с выпиленными айдишниками
    """

    def rmv_ids(node):
        remove_keys = []
        if isinstance(node, dict):
            for key, value in node.items():
                rmv_ids(value)
                if key == 'id':
                    remove_keys.append(key)
            for key in remove_keys:
                del node[key]
        elif isinstance(node, list):
            for item in node:
                rmv_ids(item)

    res = origin_dict.copy()
    rmv_ids(res)
    return res


def compare_json_left_in_right(json1, json2, key='', path=''):
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
                diff_dict[key] = {"expected": json1[key], "actual": "key undefined", "path": f"{path}{key}"}
                continue
            diff_dict.update(compare_json_left_in_right(json1[key], json2[key], key, f"{path}{key}:"))
    elif json1 != json2:
        diff_dict[key] = {"expected": json1, "actual": json2, "path": path[:-1]}
    return diff_dict
