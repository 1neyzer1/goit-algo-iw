from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Set, Tuple
import random
import math


# ================== ЗАВДАННЯ 1: СКЛАДАННЯ РОЗКЛАДУ ЗАНЯТЬ ==================

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


# ================== ЗАВДАННЯ 2: ЛОКАЛЬНИЙ ПОШУК ==================

def sphere_function(x: List[float]) -> float:
    """Функція Сфери: f(x) = Σ(xi²)"""
    return sum(xi ** 2 for xi in x)


def hill_climbing(func, bounds: List[Tuple[float, float]], iterations: int = 1000, 
                   epsilon: float = 1e-6) -> Tuple[List[float], float]:
    """
    Алгоритм підйому на гору (Hill Climbing).
    
    Args:
        func: Функція мінімізації
        bounds: Межі для кожного параметра [(min1, max1), (min2, max2), ...]
        iterations: Максимальна кількість ітерацій
        epsilon: Точність сходження
    
    Returns:
        Кортеж (оптимальна точка, значення функції)
    """
    # Ініціалізація випадковою точкою
    current_x = [random.uniform(low, high) for low, high in bounds]
    current_value = func(current_x)
    
    for iteration in range(iterations):
        # Генеруємо сусідню точку з невеликим збуренням
        neighbor_x = current_x.copy()
        dimension = random.randint(0, len(bounds) - 1)
        step_size = (bounds[dimension][1] - bounds[dimension][0]) * 0.01
        neighbor_x[dimension] += random.uniform(-step_size, step_size)
        
        # Обмежуємо межами
        neighbor_x[dimension] = max(bounds[dimension][0], 
                                    min(bounds[dimension][1], neighbor_x[dimension]))
        
        neighbor_value = func(neighbor_x)
        
        # Якщо сусід кращий, переходимо до нього
        if neighbor_value < current_value:
            if abs(neighbor_value - current_value) < epsilon:
                return current_x, current_value
            current_x = neighbor_x
            current_value = neighbor_value
        else:
            # Якщо немає поліпшення декілька разів, зупиняємся
            if iteration > 0 and abs(current_value - func(current_x)) < epsilon:
                break
    
    return current_x, current_value


def random_local_search(func, bounds: List[Tuple[float, float]], iterations: int = 1000,
                        epsilon: float = 1e-6) -> Tuple[List[float], float]:
    """
    Випадковий локальний пошук (Random Local Search).
    
    Args:
        func: Функція мінімізації
        bounds: Межі для кожного параметра
        iterations: Максимальна кількість ітерацій
        epsilon: Точність сходження
    
    Returns:
        Кортеж (оптимальна точка, значення функції)
    """
    best_x = [random.uniform(low, high) for low, high in bounds]
    best_value = func(best_x)
    prev_value = best_value
    
    for iteration in range(iterations):
        # Генеруємо випадкову сусідню точку
        neighbor_x = best_x.copy()
        dimension = random.randint(0, len(bounds) - 1)
        step_size = (bounds[dimension][1] - bounds[dimension][0]) * 0.02
        neighbor_x[dimension] += random.uniform(-step_size, step_size)
        
        # Обмежуємо межами
        neighbor_x[dimension] = max(bounds[dimension][0],
                                    min(bounds[dimension][1], neighbor_x[dimension]))
        
        neighbor_value = func(neighbor_x)
        
        # Приймаємо кращого сусіда
        if neighbor_value < best_value:
            best_x = neighbor_x
            best_value = neighbor_value
        
        # Перевіряємо сходження
        if abs(best_value - prev_value) < epsilon:
            break
        prev_value = best_value
    
    return best_x, best_value


def simulated_annealing(func, bounds: List[Tuple[float, float]], iterations: int = 1000,
                        temp: float = 1000, cooling_rate: float = 0.95,
                        epsilon: float = 1e-6) -> Tuple[List[float], float]:
    """
    Імітація відпалу (Simulated Annealing).
    
    Args:
        func: Функція мінімізації
        bounds: Межі для кожного параметра
        iterations: Максимальна кількість ітерацій
        temp: Початкова температура
        cooling_rate: Коефіцієнт охолодження (0 < cooling_rate < 1)
        epsilon: Точність сходження
    
    Returns:
        Кортеж (оптимальна точка, значення функції)
    """
    current_x = [random.uniform(low, high) for low, high in bounds]
    current_value = func(current_x)
    best_x = current_x.copy()
    best_value = current_value
    
    current_temp = temp
    
    for iteration in range(iterations):
        # Перевіряємо температуру
        if current_temp < epsilon:
            break
        
        # Генеруємо сусідню точку
        neighbor_x = current_x.copy()
        dimension = random.randint(0, len(bounds) - 1)
        step_size = (bounds[dimension][1] - bounds[dimension][0]) * 0.05
        neighbor_x[dimension] += random.uniform(-step_size, step_size)
        
        # Обмежуємо межами
        neighbor_x[dimension] = max(bounds[dimension][0],
                                    min(bounds[dimension][1], neighbor_x[dimension]))
        
        neighbor_value = func(neighbor_x)
        
        # Різниця значень
        delta = neighbor_value - current_value
        
        # Критерій прийняття (завжди приймаємо кращі, іноді гірші)
        if delta < 0 or random.random() < math.exp(-delta / current_temp):
            current_x = neighbor_x
            current_value = neighbor_value
            
            # Оновлюємо найкращу знайдену точку
            if current_value < best_value:
                best_x = current_x.copy()
                best_value = current_value
        
        # Охолоджуємо
        current_temp *= cooling_rate
    
    return best_x, best_value


def run_task1():
    """Запуск Завдання 1: Складання розкладу занять"""
    print("=" * 60)
    print("ЗАВДАННЯ 1: СКЛАДАННЯ РОЗКЛАДУ ЗАНЯТЬ")
    print("=" * 60)
    
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
        print('\nРозклад занять:')
        for teacher in schedule:
            print(
                f"{teacher.first_name} {teacher.last_name}, {teacher.age} років, "
                f"email: {teacher.email}"
            )
            print(f"   Викладає предмети: {', '.join(teacher.assigned_subjects)}\n")
    else:
        print('Неможливо покрити всі предмети наявними викладачами.')


def run_task2():
    """Запуск Завдання 2: Локальний пошук"""
    print("\n" + "=" * 60)
    print("ЗАВДАННЯ 2: ЛОКАЛЬНИЙ ПОШУК")
    print("=" * 60)
    
    # Межі для функції Сфери
    bounds = [(-5, 5), (-5, 5)]
    
    # Hill Climbing
    print("\n1. Hill Climbing (Підйом на гору):")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print(f"   Розв'язок: {hc_solution}")
    print(f"   Значення функції: {hc_value}")
    
    # Random Local Search
    print("\n2. Random Local Search (Випадковий локальний пошук):")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print(f"   Розв'язок: {rls_solution}")
    print(f"   Значення функції: {rls_value}")
    
    # Simulated Annealing
    print("\n3. Simulated Annealing (Імітація відпалу):")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print(f"   Розв'язок: {sa_solution}")
    print(f"   Значення функції: {sa_value}")


if __name__ == '__main__':
    run_task1()
    run_task2()
