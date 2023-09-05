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


def compare_json_left_in_right(json1, json2):
    """
    Сравнивает значения 2 json. Берет значения полей json1 и сравнивает их со значениями полей json2. Проверяются только
    поля, которые есть в json1.
    Если код находит поле с таким же ключом в другом json, то происходит сравнение их значений:
        - Если в поле находится другой json, то рекурсивно сравниваются значения его полей.
        - Если в поле находится список, то сравниваются значения этих списков. Если списки разной длины,
            то код не сравнивает их значения, а кладет в результат сами списки.
        - Если в поле находится единичное значение, то сравниваются эти значения.

    :return: list [tuple (ключ поля, значение этого поля из json1, значение этого поля из json2)]
    """
    diff = []
    for key in json1:
        # if isinstance(key, dict):
        #     compare_json_left_in_right(key, json2)
        if isinstance(json1[key], dict) and isinstance(json2[key], dict):
            nested_diff = compare_json_left_in_right(json1[key], json2[key])
            if nested_diff:
                diff.extend(nested_diff)
        elif isinstance(json1[key], list) and isinstance(json2[key], list):
            if len(json1[key]) != len(json2[key]):
                diff.append((key, json1[key], json2[key]))
            else:
                for i, item in enumerate(json1[key]):
                    if isinstance(item, (dict, list)) and isinstance(json2[key][i], (dict, list)):
                        nested_diff = compare_json_left_in_right(item, json2[key][i])
                        diff.extend(nested_diff)
                    elif item != json2[key][i]:
                        diff.append((f'{key}[{i}]', item, json2[key][i]))
        elif json1[key] != json2[key]:
            diff.append((key, json1[key], json2[key]))
    return diff


js1 = {
    "data": {
        "kaban": None,
        "color": "Cloudy Whit",
        "capacity": {
            "test": "sdkjf",
            "test2": "sdkjf"
        }
    }
}

js2 = {
    "data": {
        "lala": 1,
        "color": "Cloudy Whit",
        "capacity": {
            "test": None
        }
    }
}

"""
лишние ключи из левого json - игнорируются

для dict:
несовпание по типу -> значения левого и правого ключей
отсутствие ключа в правом json -> значения левого и правого None
несовпание по значению -> значения левого и правого ключей
"""


def comp_json_left_in_right(json1, json2, key=None, path=''):
    diff_dict = {}
    if isinstance(json1, dict) and isinstance(json2, dict):
        for key in json1:
            if key not in json2:
                diff_dict[key] = (json1[key], "key undefined", f"{path}{key}")
                continue
            diff_dict.update(comp_json_left_in_right(json1[key], json2[key], key, f"{path}{key}:"))
    elif json1 != json2:
        diff_dict[key] = (json1, json2, path[:-1])
    return diff_dict


res = comp_json_left_in_right(js1, js2)
pass
