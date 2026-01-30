from __future__ import annotations

from dataclasses import dataclass, field
import math
import random
from typing import Iterable, List, Optional, Sequence, Set, Tuple


@dataclass
class Teacher:
    first_name: str
    last_name: str
    age: int
    email: str
    can_teach_subjects: Set[str]
    assigned_subjects: Set[str] = field(default_factory=set)


def create_schedule(subjects: Iterable[str], teachers: Iterable[Teacher]) -> Optional[List[Teacher]]:
    uncovered_subjects = set(subjects)
    remaining_teachers = list(teachers)
    schedule: List[Teacher] = []

    while uncovered_subjects:
        best_teacher = None
        best_coverage: Set[str] = set()

        for teacher in remaining_teachers:
            coverage = teacher.can_teach_subjects & uncovered_subjects
            if len(coverage) > len(best_coverage):
                best_teacher = teacher
                best_coverage = coverage
            elif len(coverage) == len(best_coverage) and coverage:
                if best_teacher is None or teacher.age < best_teacher.age:
                    best_teacher = teacher
                    best_coverage = coverage

        if best_teacher is None or not best_coverage:
            return None

        best_teacher.assigned_subjects = best_coverage
        schedule.append(best_teacher)
        uncovered_subjects -= best_coverage
        remaining_teachers.remove(best_teacher)

    return schedule


if __name__ == '__main__':
    subjects = {
        'Математика',
        'Фізика',
        'Хімія',
        'Інформатика',
        'Біологія',
    }

    teachers = [
        Teacher(
            first_name='Олександр',
            last_name='Іваненко',
            age=45,
            email='o.ivanenko@example.com',
            can_teach_subjects={'Математика', 'Фізика'},
        ),
        Teacher(
            first_name='Марія',
            last_name='Петренко',
            age=38,
            email='m.petrenko@example.com',
            can_teach_subjects={'Хімія'},
        ),
        Teacher(
            first_name='Сергій',
            last_name='Коваленко',
            age=50,
            email='s.kovalenko@example.com',
            can_teach_subjects={'Інформатика', 'Математика'},
        ),
        Teacher(
            first_name='Наталія',
            last_name='Шевченко',
            age=29,
            email='n.shevchenko@example.com',
            can_teach_subjects={'Біологія', 'Хімія'},
        ),
        Teacher(
            first_name='Дмитро',
            last_name='Бондаренко',
            age=35,
            email='d.bondarenko@example.com',
            can_teach_subjects={'Фізика', 'Інформатика'},
        ),
        Teacher(
            first_name='Олена',
            last_name='Гриценко',
            age=42,
            email='o.grytsenko@example.com',
            can_teach_subjects={'Біологія'},
        ),
    ]

    schedule = create_schedule(subjects, teachers)

    if schedule:
        print('Розклад занять:')
        for teacher in schedule:
            print(
                f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, "
                f"email: {teacher.email}"
            )
            print(f" Викладає предмети: {', '.join(teacher.assigned_subjects)}\n")
    else:
        print('Неможливо покрити всі предмети наявними викладачами.')

    print('\n' + '-' * 40 + '\n')

    def sphere_function(point: Sequence[float]) -> float:
        return sum(value**2 for value in point)

    def _random_point(bounds: Sequence[Tuple[float, float]]) -> List[float]:
        return [random.uniform(low, high) for low, high in bounds]

    def _clip_point(point: Sequence[float], bounds: Sequence[Tuple[float, float]]) -> List[float]:
        return [
            max(min(value, high), low)
            for value, (low, high) in zip(point, bounds, strict=True)
        ]

    def hill_climbing(
        func,
        bounds: Sequence[Tuple[float, float]],
        iterations: int = 1000,
        epsilon: float = 1e-6,
        step_size: float = 0.1,
    ) -> Tuple[List[float], float]:
        current = _random_point(bounds)
        current_value = func(current)

        for _ in range(iterations):
            candidate = [
                value + random.uniform(-step_size, step_size)
                for value in current
            ]
            candidate = _clip_point(candidate, bounds)
            candidate_value = func(candidate)

            if candidate_value < current_value:
                improvement = abs(current_value - candidate_value)
                movement = math.dist(current, candidate)
                current, current_value = candidate, candidate_value
                if improvement < epsilon and movement < epsilon:
                    break
            else:
                if step_size > epsilon:
                    step_size *= 0.99

        return current, current_value

    def random_local_search(
        func,
        bounds: Sequence[Tuple[float, float]],
        iterations: int = 1000,
        epsilon: float = 1e-6,
    ) -> Tuple[List[float], float]:
        best = _random_point(bounds)
        best_value = func(best)

        for _ in range(iterations):
            candidate = _random_point(bounds)
            candidate_value = func(candidate)

            if candidate_value < best_value:
                improvement = abs(best_value - candidate_value)
                movement = math.dist(best, candidate)
                best, best_value = candidate, candidate_value
                if improvement < epsilon and movement < epsilon:
                    break

        return best, best_value

    def simulated_annealing(
        func,
        bounds: Sequence[Tuple[float, float]],
        iterations: int = 1000,
        temp: float = 1000.0,
        cooling_rate: float = 0.95,
        epsilon: float = 1e-6,
        step_size: float = 0.5,
    ) -> Tuple[List[float], float]:
        current = _random_point(bounds)
        current_value = func(current)
        best = current[:]
        best_value = current_value

        for _ in range(iterations):
            if temp < epsilon:
                break

            candidate = [
                value + random.uniform(-step_size, step_size)
                for value in current
            ]
            candidate = _clip_point(candidate, bounds)
            candidate_value = func(candidate)

            delta = candidate_value - current_value
            if delta < 0 or random.random() < math.exp(-delta / temp):
                movement = math.dist(current, candidate)
                current, current_value = candidate, candidate_value
                if current_value < best_value:
                    improvement = abs(best_value - current_value)
                    best, best_value = current[:], current_value
                    if improvement < epsilon and movement < epsilon:
                        break

            temp *= cooling_rate

        return best, best_value

    bounds = [(-5, 5), (-5, 5)]

    print('Hill Climbing:')
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print('Розв\'язок:', hc_solution, 'Значення:', hc_value)

    print('\nRandom Local Search:')
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print('Розв\'язок:', rls_solution, 'Значення:', rls_value)

    print('\nSimulated Annealing:')
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print('Розв\'язок:', sa_solution, 'Значення:', sa_value)
