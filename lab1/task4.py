tasks = {}


def add_task(name, status):
    tasks[name] = status


def change_status(name, new_status):
    if name in tasks:
        tasks[name] = new_status
    else:
        print("Такої задачі не існує")


def delete_task(name):
    if name in tasks:
        del tasks[name]
    else:
        print("Такої задачі не існує")


while True:
    print("\nМеню:")
    print("1 - Додати задачу")
    print("2 - Змінити статус задачі")
    print("3 - Видалити задачу")
    print("4 - Показати всі задачі")
    print("0 - Вийти")

    choice = input("Ваш вибір: ")

    if choice == "1":
        name = input("Назва задачі: ")
        status = input("Статус (виконано / в процесі / очікує): ")
        add_task(name, status)

    elif choice == "2":
        name = input("Назва задачі: ")
        new_status = input("Новий статус (виконано / в процесі / очікує): ")
        change_status(name, new_status)

    elif choice == "3":
        name = input("Назва задачі: ")
        delete_task(name)

    elif choice == "4":
        print("Список задач:", tasks)

    elif choice == "0":
        break

    else:
        print("Невірний вибір")

waiting_tasks = [task for task, status in tasks.items() if status == "очікує"]
print("Задачі в очікуванні:", waiting_tasks)
