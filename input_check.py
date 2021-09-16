import re


def answer_validate(answer):
    """Validates the user response for the presence of numbers"""
    filtered_answer = answer.replace(',', '.')
    # Replacing Cyrillic 'е' with 'Е' in the case of an exponential form
    filtered_answer = filtered_answer.replace('\u0435', 'e').replace('\u0415', 'E')
    try:
        # Searching for a real number (including exponential form)
        filtered_answer = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", filtered_answer)

        filtered_answer = round(float(filtered_answer.group(0)), 1)  # Round up for a clean display
        if filtered_answer > 0:
            return filtered_answer if filtered_answer % 1 > 0 else int(filtered_answer)  # for a clean display
        else:
            return "Значние отрицательное или слишком мало, попробуй еще раз"
    except:
        return "Неверный формат, попробуй еще раз"


def state_translate(name_of_state):
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
