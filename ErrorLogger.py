import os
from collections import defaultdict

class ErrorLogger:
    errors_value = 0
    E_Notification: str = 'Уведомления'
    E_Patch_Notification: str = 'Уведомления патчей'
    E_Major: str = 'Серьезные ошибки'
    E_Minor: str = 'Малые ошибки'

    def __init__(self):
        # Структура данных:
        # {
        #   "Категория": {
        #       "Уникальный ключ ошибки": {
        #           "message": "Текст ошибки",
        #           "solution": "Текст решения",
        #           "files": set("путь_к_файлу1", "путь_к_файлу2", ...)
        #       }
        #   }
        # }
        self.errors = defaultdict(lambda: defaultdict(lambda: {'files': set(), 'message': '', 'solution': ''}))

    def add_error(self, category, file_path, message, solution=None, error_key=None):
        self.errors_value += 1
        """
        Добавляет ошибку в лог.

        :param category: Название раздела (например, 'Серьезные ошибки')
        :param file_path: Путь к файлу, в котором найдена ошибка
        :param message: Описание ошибки (без названия файла)
        :param solution: Как исправить (опционально)
        :param error_key: Уникальный ключ для группировки. Если None, используется message.
        """
        # Если ключ не задан, используем сообщение как ключ группировки
        key = error_key if error_key is not None else message

        entry = self.errors[category][key]
        entry['files'].add(file_path)
        entry['message'] = message
        if solution:
            entry['solution'] = solution

    def save_report(self, filepath="error_log2.txt"):
        """Сохраняет накопленный отчет в файл."""

        if self.errors_value == 0:
            return

        # Определяем порядок категорий (сначала важные)
        category_order = [
            self.E_Notification,
            self.E_Major,
            self.E_Minor,
            self.E_Patch_Notification
        ]

        # Добавляем любые новые категории, которые могли появиться, в конец списка
        for cat in self.errors:
            if cat not in category_order:
                category_order.append(cat)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("ОТЧЕТ ОБ ОШИБКАХ\n")
            f.write("=" * 50 + "\n\n")


            for category in category_order:
                if category not in self.errors:
                    continue

                f.write(f"### {category.upper()} ###\n")
                f.write("-" * 50 + "\n")

                for key, data in self.errors[category].items():
                    files_list = sorted(list(data['files']))  # Сортируем файлы по алфавиту

                    f.write(f"\nОШИБКА: {data['message']}\n")
                    if data['solution']:
                        f.write(f"РЕШЕНИЕ: {data['solution']}\n")

                    for file_path in files_list:
                        f.write(f"  - {file_path}\n")

                    f.write("-" * 20 + "\n")

                f.write("\n" + "=" * 50 + "\n\n")

        print(f"Отчет сохранен в файл: {os.path.abspath(filepath)}")


# --- ПРИМЕР ИСПОЛЬЗОВАНИЯ ---

logger = ErrorLogger()

"""
        mes = {
            'ru':"Папка мода существует, но без About.xml\nФайл не может быть прочитан программой. Возможные причины: файл не существует, поврежден, неправильная кодировка.",
            'en':"The mod folder exists, but without About.xml\nThe file cannot be read by the program. Possible reasons: the file does not exist, is corrupted, or the encoding is incorrect.",
            'es':"La carpeta mod existe, pero sin About.xml\nEl programa no puede leer el archivo. Posibles motivos: el archivo no existe, está dañado o la codificación es incorrecta.",
        }

        sol = {
            'ru':"Это, Возможно, просто не до конца удалённый мод. Если это так, то лучше удалить всю папку.",
            'en':"It's probably just a not-fully-deleted mod. If so, it is better to delete the entire folder.",
            'es':"Puede que simplemente no sea un mod completamente remoto. Si es así, es mejor eliminar toda la carpeta.",

        }

        logger.add_error(
            category=logger.E_Notification,
            file_path=str(file),
            message=mes[SVV.Settings_language],
            solution=sol[SVV.Settings_language],
        )


"""


