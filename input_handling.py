import re
from aiogram.utils.exceptions import MessageToEditNotFound, MessageNotModified
from data_base.sqlite_db_OOP import DBCommands
from loader import bot


async def number_search(answer: str) -> [float, str]:
    """Searches for a number in a string"""
    filtered_answer = answer.replace(',', '.')
    filtered_answer = filtered_answer.replace('\u0435', 'e').replace('\u0415', 'E')  # Replacing Cyrillic 'е' and 'Е'
    filtered_answer = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", filtered_answer)
    if filtered_answer:
        return round(float(filtered_answer.group(0)), 1)
    else:
        return "Неверный формат, попробуй еще раз"


async def answer_validate(answer: str) -> [float, str]:
    """Validates the user answer in terms of a positive number"""
    if answer.isdigit() and float(answer) > 0:
        return float(answer)
    else:
        valid_answer = await number_search(answer)
        if isinstance(valid_answer, str):
            return valid_answer
        elif float(valid_answer) >= 0:
            return float(valid_answer)
        else:
            return "Введи положительное число"


async def state_translate(state_name: str, question=False) -> str:
    """Returns a polling request or translation of the state name in Russian"""
    state_name_without_prefix = (re.findall(r'\w+$', state_name))[0]
    match state_name_without_prefix:
        case 'body_weight':
            return 'Введи свой вес' if question else 'Вес'
        case 'body_height':
            return 'Введи свой рост' if question else 'Рост'
        case 'foot':
            return 'Введи длину ступни' if question else 'Длина ступни'
        case 'ankle_to_ground':
            return 'Введи высоту голеностопа' if question else 'Высота голеностопа'
        case 'tibia':
            return 'Введи длину голени' if question else 'Длина голени'
        case 'femur':
            return 'Введи длину бедра' if question else 'Длина бедра'
        case 'pelvis':
            return 'Введи высоту таза' if question else 'Высота таза'
        case 'torso':
            return 'Введи длину торса' if question else 'Длина торса'
        case 'head_and_neck':
            return 'Введи высоту шеи и головы' if question else 'Высота шеи и головы'
        case 'humerus':
            return 'Введи длину плеча' if question else 'Длина плеча'
        case 'forearm':
            return 'Введи длину предплечья' if question else 'Длина предплечья'
        case 'hand':
            return 'Введи длину кисти' if question else 'Длина кисти'
        case 'number_of_reps':
            return 'Введи количество повторений' if question else 'Количество по вторений'
        case 'number_of_sets':
            return 'Введи количество подходов' if question else 'Количество подходов'


async def put_question_message_id(question, state):
    """Puts the question message id with inline buttons in state data"""
    async with state.proxy() as data:
        data['question_message_id'] = question.message_id


async def delete_reply_markup(message, state):
    """Deletes inline buttons"""
    async with state.proxy() as data:
        question_message_id = data['question_message_id'] if 'question_message_id' in data else None
    try:
        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=question_message_id,
                                            reply_markup=None)
    except MessageToEditNotFound:
        pass
    except MessageNotModified:
        pass


async def close_anthropometry_state(state):
    """Closes the state of anthropometry and puts data (body part length) to the database"""
    async with state.proxy() as data:
        data.pop('question_message_id')
        reversed_tuple = tuple([t[::-1] for t in tuple(data.items())])
    anthropometry_db = DBCommands('anthropometry', 'body_part_name', 'body_part_length', 'body_part_weight')
    await anthropometry_db.db_update('body_part_length', 'body_part_name', reversed_tuple)
    await state.reset_state()
