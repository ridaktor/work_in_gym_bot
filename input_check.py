import re


def _number_search(answer: str) -> [float, str]:
    """Searches for a number in a string"""
    filtered_answer = answer.replace(',', '.')
    filtered_answer = filtered_answer.replace('\u0435', 'e').replace('\u0415', 'E')  # Replacing Cyrillic 'е' and 'Е'
    filtered_answer = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", filtered_answer)
    if filtered_answer:
        return round(float(filtered_answer.group(0)), 1)
    else:
        return "Неверный формат, попробуй еще раз"


def _answer_validate(answer: str) -> [float, int, str]:
    """Validates the user answer in terms of a positive number"""
    if answer.isdigit() and int(answer) > 0:
        return int(answer)
    else:
        valid_answer = _number_search(answer)
        if isinstance(valid_answer, str):
            return valid_answer
        elif valid_answer > 0:
            return valid_answer if valid_answer % 1 > 0 else int(valid_answer)  # for a clean display
        else:
            return "Значние отрицательное или слишком мало, попробуй еще раз"


def _state_translate(name_of_state: str) -> str:
    """Translates the name of state into Russian"""
    result = re.findall(r'\w+$', name_of_state)
    sub_dict = {
        'body_weight': 'вес',
        'body_height': 'рост',
        'foot': 'ступня',
        'ankle_to_ground': 'голеностоп',
        'tibia': 'голень',
        'femur': 'бедро',
        'pelvis': 'таз',
        'torso': 'торс',
        'head_and_neck': 'шея и голова',
        'humerus': 'плечо',
        'forearm': 'предплечье',
        'hand': 'кисть'
    }
    regex = '|'.join(sub_dict)
    return re.sub(regex, lambda m: sub_dict[m.group()], str(result[0]))
