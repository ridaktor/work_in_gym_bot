class Exercise:
    g = 9.81

    def __init__(self, name_of_exercise, extra_weight, reps, sets):
        self.name_of_exercise = name_of_exercise
        self.extra_weight = extra_weight
        self.reps = reps
        self.sets = sets

    def get_work(self):
        if self.name_of_exercise == 'Приседания':
            return self.sets * self.extra_weight * self.g * self.reps * 0.01
        else:
            print('Такого упражнения нет')

