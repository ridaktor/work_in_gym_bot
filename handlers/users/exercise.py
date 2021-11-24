from app import exercise_db


class Exercise:
    g = 9.81

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

    def __init__(self, name_of_exercise, extra_weight, numb_of_reps, numb_of_sets):
        self.name_of_exercise = name_of_exercise
        self.extra_weight = extra_weight
        self.numb_of_reps = numb_of_reps
        self.numb_of_sets = numb_of_sets
        # self.moved_distance = Exercise.movements[self.name_of_exercise]['moved_distance']
        # self.sprung_weight = Exercise.movements[self.name_of_exercise]['sprung_weight']

    async def _get_movements(self, movement):
        if movement == 'sprung_weight':
            answer = \
                list(await exercise_db.db_read('sprung_weight', "exercise_name = '{}'".format(self.name_of_exercise)))[
                    0][0]
            return answer
        else:
            answer = \
                list(await exercise_db.db_read('moved_distance', "exercise_name = '{}'".format(self.name_of_exercise)))[
                    0][
                    0]
            return answer

    async def get_work(self):
        """Returns the work done in Joules"""
        sprung_weight = await self._get_movements('sprung_weight')
        moved_distance = await self._get_movements('moved_distance')
        return self.numb_of_sets * (
                (sprung_weight + self.extra_weight) * self.g * moved_distance * self.numb_of_reps * 0.01)
