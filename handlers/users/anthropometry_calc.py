import asyncio

from data_base.sqlite_db import db_read

# db_data = dict(await db_read())
# body_weight = db_data['body_weight']  # body weight in kg
# headless_weight = body_weight \
#                   - (19.36 + 0.001722 * (body_weight ** 2)) ** 0.5  # weight without weight of head and neck in kg
# component_weight = {'head_and_neck': body_weight - headless_weight,
#                     'torso': 0.007452 * headless_weight * db_data['torso'],
#                     'pelvis': 0.00696 * headless_weight * db_data['pelvis'],
#                     'femur': 0.00715 * headless_weight * db_data['femur'],
#                     'tibia': 0.00273 * headless_weight * db_data['tibia'],
#                     'ankle_to_ground': None,
#                     'foot': 0.000699 * headless_weight * db_data['foot'],
#                     'humerus': 0.00188 * headless_weight * db_data['humerus'],
#                     'forearm': 0.00144 * headless_weight * db_data['forearm'],
#                     'hand': 0.000681 * headless_weight * db_data['hand']
#                     }
# # vertical height from floor to top of collarbone in cm
# acromion_height = db_data['torso'] + db_data['pelvis'] + db_data['femur'] \
#                   + db_data['tibia'] + db_data['ankle_to_ground']
# # vertical height from floor to wrist with arms fully extended overhead in cm
# overhead_height = db_data['torso'] + db_data['pelvis'] + db_data['femur'] \
#                   + db_data['tibia'] + db_data['ankle_to_ground'] + db_data['humerus'] \
#                   + db_data['forearm']
# # vertical height from floor to head top in cm
# overall_height = db_data['head_and_neck'] + db_data['torso'] + db_data['pelvis'] \
#                  + db_data['femur'] + db_data['tibia'] + db_data['ankle_to_ground']
