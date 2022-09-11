from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Ergebnis der Programm"""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Training Type: {self.training_type}; '
                f'{self.duration:.3f} St. lang; '
                f'Distance: {self.distance:.3f} km; '
                f'Mittel Schnellheit: {self.speed:.3f} km/st; '
                f'{self.calories:.3f} Calories verloren.')


class Training:
    """Mutter-Class, Funktionen die wereden
    von allen anderen Classen benutzt"""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Distanse in KM"""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Mittel-Schnellheit"""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        pass

    def show_training_info(self) -> InfoMessage:
        """Ein Info-Message ausgeben"""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training Joggen (personliche Funktionen dieses Classes)"""
    RUN_CALORIES_MULTIPLER_COEFF: int = 18
    RUN_CALORIES_MULTIPLER_COEFF_2: int = 20

    def get_spent_calories(self) -> float:
        FIRST_STEP = self.RUN_CALORIES_MULTIPLER_COEFF * self.get_mean_speed()
        SECOND_STEP = FIRST_STEP - self.RUN_CALORIES_MULTIPLER_COEFF_2
        THIRD_STEP = SECOND_STEP * self.weight / self.M_IN_KM
        return THIRD_STEP * (self.duration * self.MINUTES_IN_HOUR)


class SportsWalking(Training):
    """Trainig Sportgehen (personliche Funktionen dieses Classes)"""
    SPORTWALK_CALORIES_MULTIPLER_COEFF: float = 0.035
    SPORTWALK_CALORIES_MULTIPLER_COEFF_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.SPORTWALK_CALORIES_MULTIPLER_COEFF
                * self.weight
                + (self.get_mean_speed()
                    ** 2
                    // self.height)
                * self.SPORTWALK_CALORIES_MULTIPLER_COEFF_2
                * self.weight)
                * self.duration
                * self.MINUTES_IN_HOUR)


class Swimming(Training):
    '''Training Schwimmen (personliche Funktionen dieses Classes)'''
    LEN_STEP: float = 1.38
    FIRST_SWIM_CALORIES_COEFF: float = 1.1
    SECOND_SWIM_CALORIES_COEFF: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        '''Wie vile calories?'''
        FIRST_STEP = (self.get_mean_speed() + self.FIRST_SWIM_CALORIES_COEFF)
        return FIRST_STEP * self.SECOND_SWIM_CALORIES_COEFF * self.weight


def read_package(train: str, data: list) -> Training:
    """Daten lesen"""
    tranings = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if train in tranings:
        return tranings[train](*data)
    else:
        raise ValueError


def main(training: Training) -> None:
    """Main Funktion"""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
