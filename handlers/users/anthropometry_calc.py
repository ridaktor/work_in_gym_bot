import math
from app import anthropometry_db, exercise_db


async def shortening(height, angle):
    """Takes height and angle and returns the height change"""
    return math.sqrt(height ** 2 * math.cos(math.radians(angle)) ** 2)


async def fill_body_part_weight_column():
    """Fills body_part_weight column in anthropometry_db"""
    body_part_value = dict(await anthropometry_db.db_read('body_part_name, body_part_value'))
    body_weight = body_part_value['body_weight']
    headless_weight = body_weight - (19.36 + 0.001722 * (body_weight ** 2)) ** 0.5  # RMS of the reference and the input

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

    # vertical height from floor to head top in cm
    overall_height = sum(
        body_part_value[key] for key in ['head_and_neck', 'torso', 'pelvis', 'femur', 'tibia', 'ankle_to_ground'])
    return True if abs(overall_height - body_part_value['body_height']) > 10 or \
                   any(v == 0 for v in body_part_value.values()) else False


async def fill_movements():
    """"""
    body_part_weight = dict(await anthropometry_db.db_read('body_part_name, body_part_weight'))
    body_part_value = dict(await anthropometry_db.db_read('body_part_name, body_part_value'))
    movements = {'Приседания': {'sprung_weight': body_part_weight['femur'] / (2 * math.sin(math.radians(83 - 13)))
                                                 + sum(body_part_weight[key] for key in ['head_and_neck', 'torso',
                                                                                         'pelvis', 'humerus', 'forearm',
                                                                                         'hand']),
                                'moved_distance': await shortening(body_part_value['tibia'], 10)
                                                  + await shortening(body_part_value['femur'], 13)
                                                  + await shortening(
                                    body_part_value['pelvis'] + body_part_value['torso'], 11)
                                                  - await shortening(body_part_value['tibia'], 36)
                                                  - await shortening(body_part_value['femur'], 83)
                                                  - await shortening(
                                    body_part_value['pelvis'] + body_part_value['torso'], 39)
                                },
                 'Румынская тяга': {'sprung_weight': (body_part_weight['torso'] + body_part_weight['pelvis']) / (
                         2 * math.sin(math.radians(78)))
                                                     + sum(
                     body_part_weight[key] for key in ['head_and_neck', 'humerus', 'forearm', 'hand']),
                                    'moved_distance': sum(body_part_value[key] for key in ['pelvis', 'torso'])
                                                      + await shortening(body_part_value['tibia'], 7)
                                                      + await shortening(body_part_value['femur'], 19)
                                                      - await shortening(body_part_value['tibia'], 3)
                                                      - await shortening(body_part_value['femur'], 30)
                                                      - await shortening(
                                        body_part_value['pelvis'] + body_part_value['torso'], 78)
                                    },
                 'Подтягивания': {'sprung_weight': body_part_value['body_weight']
                                                   - body_part_weight['humerus'] * 0.5
                                                   - sum(body_part_weight[key] for key in ['forearm', 'hand']),
                                  'moved_distance': sum(body_part_value[key] for key in ['forearm', 'humerus'])
                                  },
                 'Отжимания на брусьях': {'sprung_weight': body_part_value['body_weight']
                                                           - body_part_weight['humerus'] * 0.5
                                                           - sum(body_part_weight[key] for key in ['forearm', 'hand']),
                                          'moved_distance': body_part_value['humerus']
                                          }
                 }

    list_of_data = []
    for exercise_name in movements.keys():
        dataset = []
        for movement in movements[exercise_name]:
            dataset.append(movements[exercise_name][movement])
        dataset.append(exercise_name)
        list_of_data.append(tuple(dataset))
    await exercise_db.db_update('sprung_weight, moved_distance', 'exercise_name', tuple(list_of_data))
