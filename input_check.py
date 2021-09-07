import re


async def answer_check(answer, message):
    """
    The function checks the user's answer for correctness
    """
    try:
        filtered_answer = answer.replace(',', '.')

        # replacing Cyrillic ('е' and 'Е')
        filtered_answer = filtered_answer.replace('\u0435', 'e').replace('\u0415', 'E')

        # searching for a real number (including exp. form)
        filtered_answer = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", filtered_answer)

        filtered_answer = float(filtered_answer.group(0))
        if filtered_answer > 0:
            return round(filtered_answer, 1) if filtered_answer % 1 > 0 else int(filtered_answer)  # for a clean display
        else:
            await message.answer("Введи положительное значение")
    except:
        await message.answer("Неверный формат, попробуй еще раз")
