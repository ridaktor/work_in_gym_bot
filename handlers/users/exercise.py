from app import exercise_db


class Exercise:
    g = 9.81

    def __init__(self, name_of_exercise, extra_weight, numb_of_reps, numb_of_sets):
        self.name_of_exercise = name_of_exercise
        self.extra_weight = extra_weight
        self.numb_of_reps = numb_of_reps
        self.numb_of_sets = numb_of_sets

    async def _get_moved_distance(self):
        """Gets moved distance of an exercise from database"""
        moved_distance = list(await exercise_db.db_read('moved_distance',
                                                        "exercise_name = '{}'".format(self.name_of_exercise)))[0][0]
        return moved_distance

    async def _get_sprung_weight(self):
        """Gets sprung weight of an exercise from database"""
        sprung_weight = list(await exercise_db.db_read('sprung_weight',
                                                       "exercise_name = '{}'".format(self.name_of_exercise)))[0][0]
        return sprung_weight

    async def get_work(self):
        """Returns the work done in Joules"""
        moved_distance = await self._get_moved_distance()
        sprung_weight = await self._get_sprung_weight()
        return self.numb_of_sets * ((sprung_weight + self.extra_weight) * self.g * moved_distance * self.numb_of_reps * 0.01)
