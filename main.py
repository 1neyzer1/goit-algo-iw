from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Set


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
