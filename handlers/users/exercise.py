class Exercise:
    g = 9.81

    def __init__(self, name_of_exercise, extra_weight, numb_of_reps, numb_of_sets):
        self.name_of_exercise = name_of_exercise
        self.get_exercise_params()
        self.extra_weight = extra_weight
        self.numb_of_reps = numb_of_reps
        self.numb_of_sets = numb_of_sets

    def get_exercise_params(self):
        match self.name_of_exercise:
            case 'Приседания':
                self.moved_distance = 70
                self.sprung_weight = 70
            case 'Румынская тяга':
                self.moved_distance = 60
                self.sprung_weight = 70

    def get_work(self):
        """This method returns the work done in Joules"""
        return self.numb_of_sets * (
                    (self.sprung_weight + self.extra_weight) * self.g * self.moved_distance * self.numb_of_reps * 0.01)

