import re


def answer_validation(answer):
    """Validates the user response for the presence of numbers"""
    try:
        filtered_answer = answer.replace(',', '.')

        # Replacing Cyrillic ('е' and 'Е')
        filtered_answer = filtered_answer.replace('\u0435', 'e').replace('\u0415', 'E')

        # Searching for a real number (including exp. form)
        filtered_answer = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", filtered_answer)

        # Round up for a nice display
        filtered_answer = round(float(filtered_answer.group(0)), 1)

        if filtered_answer > 0:
            return filtered_answer if filtered_answer % 1 > 0 else int(filtered_answer)  # for a clean display
        else:
            return "Значние отрицательное или слишком мало, попробуй еще раз"
    except:
        return "Неверный формат, попробуй еще раз"


def state_translator(name_of_state):
    """Translates the name of state into Russian"""
    result = re.findall(r'\w+$', name_of_state)
    sub_dict = {
        'waiting_for_body_weight': 'вес',
        'waiting_for_body_height': 'рост',
        'waiting_for_foot': 'ступня',
        'waiting_for_ankle_to_ground': 'голеностоп',
        'waiting_for_tibia': 'голень',
        'waiting_for_femur': 'бедро',
        'waiting_for_pelvis': 'таз',
        'waiting_for_torso': 'торс',
        'waiting_for_head_and_neck': 'шея и голова',
        'waiting_for_humerus': 'плечо',
        'waiting_for_forearm': 'предплечье',
        'waiting_for_hand': 'кисть'
    }
    regex = '|'.join(sub_dict)
    return re.sub(regex, lambda m: sub_dict[m.group()], str(result[0]))