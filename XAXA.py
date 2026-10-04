import datetime
import json
from typing import List, Dict, Optional


class Employee:
    def __init__(self, name: str, slots: List[datetime.datetime]):
        self.name = name
        self.slots = slots
        self.tasks: List["Task"] = []

    def add_task(self, task: "Task"):
        self.tasks.append(task)

    def get_free_slots(self) -> List[datetime.datetime]:
        busy_times = [t.slot for t in self.tasks if t.slot]
        return [s for s in self.slots if s not in busy_times]

    def to_dict(self):
        return {
            "name": self.name,
            "slots": [s.isoformat() for s in self.slots],
            "tasks": [t.to_dict() for t in self.tasks]
        }


class Task:
    def __init__(self, title: str, description: str, assigned_to: Optional[Employee] = None, slot: Optional[datetime.datetime] = None):
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.slot = slot
        self.status = "Новая"
        self.created_at = datetime.datetime.now()

    def mark_in_progress(self):
        self.status = "В работе"

    def mark_completed(self):
        self.status = "Завершена"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "assigned_to": self.assigned_to.name if self.assigned_to else None,
            "slot": self.slot.isoformat() if self.slot else None,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }


class Project:
    def __init__(self, name: str):
        self.name = name
        self.employees: List[Employee] = []
        self.tasks: List[Task] = []

    def add_employee(self, employee: Employee):
        self.employees.append(employee)

    def add_task(self, task: Task):
        self.tasks.append(task)
        if task.assigned_to:
            task.assigned_to.add_task(task)

    def get_statistics(self) -> Dict:
        total = len(self.tasks)
        if total == 0:
            return {"total": 0, "completed": 0, "in_progress": 0, "new": 0, "completion_rate": 0}
        completed = sum(1 for t in self.tasks if t.status == "Завершена")
        in_progress = sum(1 for t in self.tasks if t.status == "В работе")
        new = sum(1 for t in self.tasks if t.status == "Новая")
        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "new": new,
            "completion_rate": round(completed / total * 100, 2)
        }

    def to_dict(self):
        return {
            "name": self.name,
            "employees": [e.to_dict() for e in self.employees],
            "tasks": [t.to_dict() for t in self.tasks],
            "statistics": self.get_statistics()
        }


class Manager:
    def __init__(self, project: Project):
        self.project = project

    def show_free_slots(self):
        print("\n=== Свободные слоты сотрудников ===")
        for emp in self.project.employees:
            free = emp.get_free_slots()
            if free:
                print(f"{emp.name}: {[s.strftime('%d.%m %H:%M') for s in free]}")
            else:
                print(f"{emp.name}: нет свободных слотов")

    def assign_task(self, task_title: str, description: str, employee_name: str, slot_str: str):
        emp = next((e for e in self.project.employees if e.name == employee_name), None)
        if not emp:
            print(f"Сотрудник {employee_name} не найден")
            return

        slot = None
        try:
            slot = datetime.datetime.fromisoformat(slot_str)
        except ValueError:
            print("Неверный формат даты. Используйте YYYY-MM-DDTHH:MM:SS")
            return

        if slot not in emp.get_free_slots():
            print(f"Слот {slot_str} не свободен у {employee_name}")
            return

        task = Task(task_title, description, assigned_to=emp, slot=slot)
        self.project.add_task(task)
        print(f"Задача '{task_title}' назначена {employee_name} на {slot.strftime('%d.%m %H:%M')}")

    def show_progress(self):
        print("\n=== Прогресс по задачам ===")
        for task in self.project.tasks:
            print(f"- {task.title} ({task.status}) -> {task.assigned_to.name if task.assigned_to else 'не назначена'}")

    def show_statistics(self):
        stats = self.project.get_statistics()
        print("\n=== Статистика выполнения ===")
        print(f"Всего задач: {stats['total']}")
        print(f"Завершено: {stats['completed']}")
        print(f"В работе: {stats['in_progress']}")
        print(f"Новых: {stats['new']}")
        print(f"Процент выполнения: {stats['completion_rate']}%")

    def save_to_file(self, filename: str = "project_data.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.project.to_dict(), f, ensure_ascii=False, indent=2)
        print(f"Данные сохранены в {filename}")

    def load_from_file(self, filename: str = "project_data.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"Загружены данные из {filename}")
            print(f"Проект: {data['name']}, сотрудников: {len(data['employees'])}, задач: {len(data['tasks'])}")
        except FileNotFoundError:
            print("Файл не найден")


def main():
    project = Project("DevTeam Tracker")

    emp1 = Employee("Анна", [
        datetime.datetime(2026, 8, 5, 10, 0),
        datetime.datetime(2026, 8, 5, 14, 0),
        datetime.datetime(2026, 8, 6, 11, 0),
    ])
    emp2 = Employee("Игорь", [
        datetime.datetime(2026, 8, 5, 9, 0),
        datetime.datetime(2026, 8, 5, 15, 0),
        datetime.datetime(2026, 8, 6, 10, 0),
    ])
    emp3 = Employee("Мария", [
        datetime.datetime(2026, 8, 5, 12, 0),
        datetime.datetime(2026, 8, 6, 14, 0),
    ])

    project.add_employee(emp1)
    project.add_employee(emp2)
    project.add_employee(emp3)

    manager = Manager(project)

    manager.show_free_slots()

    manager.assign_task("Разработать API", "Создать REST API для задач", "Анна", "2026-08-05T10:00:00")
    manager.assign_task("Дизайн интерфейса", "Нарисовать макет в Figma", "Игорь", "2026-08-05T09:00:00")
    manager.assign_task("Написать тесты", "Покрыть юнит-тестами модули", "Мария", "2026-08-05T12:00:00")

    project.tasks[0].mark_in_progress()
    project.tasks[1].mark_completed()

    manager.show_free_slots()
    manager.show_progress()
    manager.show_statistics()

    manager.save_to_file()


if __name__ == "__main__":
    main()