import asyncio

from data_base.sqlite_db import db_read

#TODO
async def anthropometry_calc():
    db_data = await db_read()





    body_weight = db_data['body_weight']  # body weight in kg
    headless_weight = body_weight \
                      - (19.36 + 0.001722 * (body_weight ** 2)) ** 0.5  # weight without weight of head and neck in kg

    # length of body components in cm
    # component_length = {'head_and_neck': 30,  # from neck base to head top
    #                     'torso': 40,  # from hip bone topmost part to neck base
    #                     'pelvis': 19,  # from hip socket to hip bone topmost part
    #                     'femur': 41,  # from hip socket to the knee
    #                     'tibia': 42,  # from knee to ankle
    #                     'ankle_to_ground': 9,  # from the ankle to the ground
    #                     'foot': 26,  # from the heel to the toes
    #                     'humerus': 27,  # upper arm, from elbow to shoulder
    #                     'forearm': 25,  # from elbow to wrist
    #                     'hand': 22  # from wrist to fingertips
    #                     }

    # weight of body components in kg
    component_weight = {'head_and_neck': body_weight - headless_weight,
                        'torso': 0.007452 * headless_weight * component_length['torso'],
                        'pelvis': 0.00696 * headless_weight * component_length['pelvis'],
                        'femur': 0.00715 * headless_weight * component_length['femur'],
                        'tibia': 0.00273 * headless_weight * component_length['tibia'],
                        'ankle_to_ground': None,
                        'foot': 0.000699 * headless_weight * component_length['foot'],
                        'humerus': 0.00188 * headless_weight * component_length['humerus'],
                        'forearm': 0.00144 * headless_weight * component_length['forearm'],
                        'hand': 0.000681 * headless_weight * component_length['hand']
                        }

    # vertical height from floor to top of collarbone in cm
    acromion_height = component_length['torso'] + component_length['pelvis'] + component_length['femur'] \
                      + component_length['tibia'] + component_length['ankle_to_ground']

    # vertical height from floor to wrist with arms fully extended overhead in cm
    overhead_height = component_length['torso'] + component_length['pelvis'] + component_length['femur'] \
                      + component_length['tibia'] + component_length['ankle_to_ground'] + component_length['humerus'] \
                      + component_length['forearm']

    # vertical height from floor to head top in cm
    overall_height = component_length['head_and_neck'] + component_length['torso'] + component_length['pelvis'] \
                     + component_length['femur'] + component_length['tibia'] + component_length['ankle_to_ground']
