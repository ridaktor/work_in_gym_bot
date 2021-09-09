import re
from invocations_counter import counter


@counter
async def answer_validation(answer, message):
    """
    The function checks the user's answer for correctness
    """
    try:
        filtered_answer = answer.replace(',', '.')

        # replacing Cyrillic ('е' and 'Е')
        filtered_answer = filtered_answer.replace('\u0435', 'e').replace('\u0415', 'E')

        # searching for a real number (including exp. form)
        filtered_answer = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", filtered_answer)
        filtered_answer = round(float(filtered_answer.group(0)), 1)
        if filtered_answer > 0:
            return filtered_answer if filtered_answer % 1 > 0 else int(filtered_answer)  # for a clean display
        else:
            await message.answer("Значние отрицательное или слишком мало, попробуй еще раз")
    except:
        await message.answer("Неверный формат, попробуй еще раз")
