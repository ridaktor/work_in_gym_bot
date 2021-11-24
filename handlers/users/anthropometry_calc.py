import math
from app import anthropometry_db, exercise_db
from keyboards.default.exercise_buttons import exercise_buttons


async def shortening(height, angle):
    """Takes height and angle and returns the height change"""
    return math.sqrt(height ** 2 * math.cos(math.radians(angle)) ** 2)


async def fill_body_part_weight_column():
    """Fills body_part_weight column in anthropometry_db"""
    body_part_value = dict(await anthropometry_db.db_read('body_part_name, body_part_value'))
    body_weight = body_part_value['body_weight']
    headless_weight = body_weight - (19.36 + 0.001722 * (body_weight ** 2)) ** 0.5

    body_part_weight = {'foot': 0.000699 * headless_weight * body_part_value['foot'],
                        'ankle_to_ground': None,
                        'tibia': 0.00273 * headless_weight * body_part_value['tibia'],
                        'femur': 0.00715 * headless_weight * body_part_value['femur'],
                        'pelvis': 0.00696 * headless_weight * body_part_value['pelvis'],
                        'torso': 0.007452 * headless_weight * body_part_value['torso'],
                        'head_and_neck': body_weight - headless_weight,
                        'humerus': 0.00188 * headless_weight * body_part_value['humerus'],
                        'forearm': 0.00144 * headless_weight * body_part_value['forearm'],
                        'hand': 0.000681 * headless_weight * body_part_value['hand']
                        }

    reversed_tuple = tuple([t[::-1] for t in tuple(body_part_weight.items())])
    await anthropometry_db.db_update('body_part_weight', 'body_part_name', reversed_tuple)


async def fill_movements():
    await exercise_db.db_insert('exercise_name', list(zip(exercise_buttons)))

    # movements = {'Приседания': {'sprung_weight': body_part_weight['head_and_neck'] + body_part_weight['torso']
    #                                              + body_part_weight['pelvis']
    #                                              + body_part_weight['femur'] / (2 * math.sin(math.radians(83 - 13)))
    #                                              + body_part_weight['humerus'] + body_part_weight['forearm']
    #                                              + body_part_weight['hand'],
    #                             'moved_distance': shortening(body_part_length['tibia'], 10)
    #                                               + shortening(body_part_length['femur'], 13)
    #                                               + shortening(body_part_length['pelvis'] + body_part_length['torso'],
    #                                                            11)
    #                                               - shortening(body_part_length['tibia'], 36)
    #                                               - shortening(body_part_length['femur'], 83)
    #                                               - shortening(body_part_length['pelvis'] + body_part_length['torso'],
    #                                                            39)
    #                             },
    #              'Румынская тяга': {'sprung_weight': body_part_weight['head_and_neck']
    #                                                  + (body_part_weight['torso'] + body_part_weight['pelvis'])
    #                                                  / (2 * math.sin(math.radians(78)))
    #                                                  + body_part_weight['humerus'] + body_part_weight['forearm']
    #                                                  + body_part_weight['hand'],
    #                                 'moved_distance': shortening(body_part_length['tibia'], 7)
    #                                                   + shortening(body_part_length['femur'], 19)
    #                                                   + body_part_length['pelvis'] + body_part_length['torso']
    #                                                   - shortening(body_part_length['tibia'], 3)
    #                                                   - shortening(body_part_length['femur'], 30)
    #                                                   - shortening(
    #                                     body_part_length['pelvis'] + body_part_length['torso'], 78)
    #                                 }
    #              }


    # for exercise in exercise_list:
    #     tuple(zip(exercise_list))
    await anthropometry_db.db_update('moved_distance, sprung_weight', 'exercise_name', (('Приседания', 32, 23),
                                                                                        ('Румынская тяга', 3434, 234),
                                                                                        ('Подтягивания', 45, 234)))