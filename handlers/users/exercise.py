from app import exercise_db


class Exercise:
    g = 9.81  # Gravitational acceleration

    def __init__(self, name_of_exercise, extra_weight, numb_of_reps, numb_of_sets):
        self.name_of_exercise = name_of_exercise
        self.extra_weight = extra_weight
        self.numb_of_reps = numb_of_reps
        self.numb_of_sets = numb_of_sets

    async def _get_movements(self, movement):
        """Returns the corresponding movement from the database"""
        return list(await exercise_db.db_read(movement, "exercise_name = '{}'".format(self.name_of_exercise)))[0][0]

    async def get_work(self):
        """Returns the work done in Joules"""
        sprung_weight = await self._get_movements('sprung_weight')
        moved_distance = await self._get_movements('moved_distance')
        return self.numb_of_sets * (
                (sprung_weight + self.extra_weight) * self.g * moved_distance * self.numb_of_reps * 0.01)
