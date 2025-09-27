import re
from collections import defaultdict
from pathlib import Path


def main(FP: Path):
    # Собираем все XML файлы
    all_files = list(FP.rglob('*.xml'))

    # Словарь для отслеживания максимального номера для каждого базового имени
    base_name_counters = defaultdict(int)
    # Множество всех существующих имен (глобальная уникальность)
    all_existing_names = set()

    # Первый проход: собираем информацию о всех существующих именах
    for file in all_files:
        stem = file.stem
        all_existing_names.add(stem)

        # Определяем базовое имя и обновляем счетчик
        base_name = extract_base_name(stem)
        current_number = extract_number(stem)
        base_name_counters[base_name] = max(base_name_counters[base_name], current_number)

    # Второй проход: переименование файлов с конфликтующими именами
    for file in all_files:
        original_stem = file.stem

        # Если имя уникально - пропускаем и удаляем его из множества
        if original_stem in all_existing_names:
            all_existing_names.remove(original_stem)
            continue

        # Если имя не уникально - нужно переименовать
        base_name = extract_base_name(original_stem)

        # Находим следующее доступное уникальное имя
        new_stem = find_unique_name(base_name, base_name_counters, all_existing_names)

        # Переименовываем файл
        new_path = file.with_stem(new_stem)
        file.rename(new_path)

        # Обновляем множества
        all_existing_names.add(new_stem)
        base_name_counters[base_name] += 1

        print(f'Renamed "{file.name}" to "{new_stem}.xml"')


def extract_base_name(stem: str) -> str:
    """Извлекает базовое имя из названия файла (без числового суффикса)"""
    match = re.search(r'(\d+)$', stem)
    if match:
        return stem[:match.start()]
    return stem


def extract_number(stem: str) -> int:
    """Извлекает числовой суффикс из названия файла"""
    match = re.search(r'(\d+)$', stem)
    return int(match.group(1)) if match else 0


def find_unique_name(base_name: str, counters: defaultdict, existing_names: set) -> str:
    """Находит уникальное имя, увеличивая счетчик до тех пор, пока имя не станет уникальным"""
    while True:
        counters[base_name] += 1
        candidate = f"{base_name}{counters[base_name]}"
        if candidate not in existing_names:
            return candidate