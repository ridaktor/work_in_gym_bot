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
